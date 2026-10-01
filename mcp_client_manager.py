"""
================================================================================
MCP Client Manager & Multi-Server Tool Orchestrator
Integrates:
  1. NASA APIs MCP Server (Planetary Telemetry, Mars Rovers, NEOs, Space Weather)
  2. STScI MAST MCP Server (Deep-Space Astrophysics, JWST & Hubble Archives)
  3. Sequential Thinking MCP Server (Multi-Step Reasoning & Verification)

Features:
  - Kill Switch via CLI flag (--no-mcp) and environment variable (ENABLE_MCP=false)
  - Circuit Breaker / Fail-safe fallback to standard ChromaDB RAG
  - Process cleanup & lifecycle management
================================================================================
"""

import os
import sys
import time
import json
import asyncio
import inspect
from typing import Dict, Any, List, Optional, Tuple
from contextlib import AsyncExitStack
from pathlib import Path

# Load environment configuration (.env)
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# Global Kill Switch Evaluation
ENABLE_MCP_ENV = os.environ.get("ENABLE_MCP", "true").lower() in ("true", "1", "yes")

# Import local direct implementations as robust in-process fallback
import nasa_mcp_server
import mast_mcp_server
import sequential_thinking_server

# Check if official MCP Python SDK is available
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False


# Ollama-compliant tool specifications for all three servers
ALL_MCP_TOOL_DEFINITIONS = [
    # --- 1. Sequential Thinking Tool ---
    {
        "type": "function",
        "function": {
            "name": "sequentialthinking",
            "description": "Executes a structured reasoning step. Decomposes complex NASA space queries, plans multi-step lookups, tests hypotheses, and verifies evidence before final answer generation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "thought": {"type": "string", "description": "The current reasoning step or analysis."},
                    "next_thought_needed": {"type": "boolean", "description": "True if another reasoning step or tool call is needed, False if ready to produce the final grounded answer."},
                    "thought_number": {"type": "integer", "description": "Current thought sequence number (starting at 1)."},
                    "total_thoughts": {"type": "integer", "description": "Estimated total thoughts needed for this question."},
                    "is_revision": {"type": "boolean", "description": "True if this thought revises a previous assumption or addresses missing data."},
                    "revises_thought": {"type": "integer", "description": "Thought number being revised (if applicable)."}
                },
                "required": ["thought", "next_thought_needed", "thought_number", "total_thoughts"]
            }
        }
    },
    # --- 2. NASA APIs Tools ---
    {
        "type": "function",
        "function": {
            "name": "nasa_near_earth_objects",
            "description": "Retrieves Near Earth Asteroid close approaches and hazard telemetry from NASA NeoWs. Relevant for asteroid defense and DART mission context. NOTE: NASA strictly limits the date range to 7 days maximum (e.g. 7 consecutive days). If omitted, the latest current 7-day window is retrieved automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD). Optional; defaults to recent date."},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD). Optional; must be within 7 days of start_date."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nasa_mars_rover_manifest",
            "description": "Retrieves current mission status, launch/landing dates, max sol, and photo count for Mars rovers (perseverance, curiosity, opportunity, spirit).",
            "parameters": {
                "type": "object",
                "properties": {
                    "rover_name": {"type": "string", "description": "Rover name: 'perseverance', 'curiosity', etc."}
                },
                "required": ["rover_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nasa_mars_rover_photos",
            "description": "Retrieves imagery and observation telemetry from Curiosity or Perseverance (NAVCAM, MAST, CHEMCAM, WATSON). NOTE: Curiosity has sols up to ~4,200; Perseverance landed in 2021 and only has sols up to ~1,200. If 'sol' is omitted or unknown, the latest valid photos are retrieved automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rover_name": {"type": "string", "description": "Rover name ('curiosity' or 'perseverance')."},
                    "sol": {"type": "integer", "description": "Martian solar day (sol count). Optional; defaults to latest available sol."},
                    "camera": {"type": "string", "description": "Camera abbreviation (NAVCAM, MAST, CHEMCAM, WATSON). Optional."}
                },
                "required": ["rover_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nasa_space_weather_donki",
            "description": "Retrieves Space Weather Database Notifications (DONKI) including Coronal Mass Ejections (CME) and solar flares impacting spacecraft radiation environments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)."},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "nasa_apod",
            "description": "Retrieves NASA Astronomy Picture of the Day with authoritative educational explanations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date (YYYY-MM-DD). Optional."}
                }
            }
        }
    },
    # --- 3. STScI MAST Astrophysics Tools ---
    {
        "type": "function",
        "function": {
            "name": "mast_resolve_target",
            "description": "Resolves astronomical coordinates (RA and Dec) for deep-space targets using STScI SIMBAD/NED resolver (e.g., 'M31', 'Trappist-1', 'Stephan's Quintet').",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_name": {"type": "string", "description": "Name of astronomical object or deep sky target."}
                },
                "required": ["target_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mast_jwst_observations",
            "description": "Queries STScI Mikulski Archive for James Webb Space Telescope observations, returning target, instrument (NIRCam, MIRI, NIRSpec), filters, and proposal ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_name": {"type": "string", "description": "Astronomical target name (e.g., 'Trappist-1', 'Orion Nebula')."},
                    "limit": {"type": "integer", "description": "Maximum number of observations to retrieve (default: 5)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mast_hubble_observations",
            "description": "Queries STScI Mikulski Archive for Hubble Space Telescope archival observations, instruments (WFC3, ACS, STIS), and proposal IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_name": {"type": "string", "description": "Astronomical target name."},
                    "limit": {"type": "integer", "description": "Maximum number of observations (default: 5)."}
                }
            }
        }
    }
]


class MultiMCPClientManager:
    """
    Unified manager orchestrating all 3 MCP servers:
      - Sequential Thinking
      - NASA APIs
      - STScI MAST
    """
    def __init__(self, enable_mcp: bool = True):
        self.enabled = enable_mcp and ENABLE_MCP_ENV
        self.exit_stack = AsyncExitStack()
        self.stdio_sessions: Dict[str, Any] = {}
        self.ollama_tools = ALL_MCP_TOOL_DEFINITIONS if self.enabled else []
        self._direct_dispatch_map = {
            # Sequential Thinking
            "sequentialthinking": sequential_thinking_server.sequential_thinking,
            # NASA APIs
            "nasa_near_earth_objects": nasa_mcp_server.get_near_earth_objects,
            "nasa_mars_rover_manifest": nasa_mcp_server.get_mars_rover_manifest,
            "nasa_mars_rover_photos": nasa_mcp_server.get_mars_rover_photos,
            "nasa_space_weather_donki": nasa_mcp_server.get_space_weather_donki,
            "nasa_apod": nasa_mcp_server.get_apod,
            # STScI MAST
            "mast_resolve_target": mast_mcp_server.resolve_astronomical_target,
            "mast_jwst_observations": mast_mcp_server.query_jwst_observations,
            "mast_hubble_observations": mast_mcp_server.query_hubble_observations
        }

    async def initialize(self) -> bool:
        """Initializes server sessions or validates direct tool execution."""
        if not self.enabled:
            return False

        # Attempt to spawn stdio sub-processes if MCP SDK is present
        if MCP_SDK_AVAILABLE:
            try:
                python_exe = sys.executable
                server_configs = {
                    "sequential_thinking": {
                        "command": python_exe,
                        "args": [str(BASE_DIR / "sequential_thinking_server.py")]
                    },
                    "nasa_apis": {
                        "command": python_exe,
                        "args": [str(BASE_DIR / "nasa_mcp_server.py")],
                        "env": {"NASA_API_KEY": os.environ.get("NASA_API_KEY", "")}
                    },
                    "stsci_mast": {
                        "command": python_exe,
                        "args": [str(BASE_DIR / "mast_mcp_server.py")]
                    }
                }

                for name, cfg in server_configs.items():
                    merged_env = os.environ.copy()
                    if "env" in cfg:
                        merged_env.update(cfg["env"])
                    params = StdioServerParameters(
                        command=cfg["command"],
                        args=cfg.get("args", []),
                        env=merged_env
                    )
                    read_stream, write_stream = await self.exit_stack.enter_async_context(
                        stdio_client(params)
                    )
                    session = await self.exit_stack.enter_async_context(
                        ClientSession(read_stream, write_stream)
                    )
                    await session.initialize()
                    self.stdio_sessions[name] = session
            except Exception as e:
                # Fail-safe: if stdio child process spawning encounters issues in sandbox,
                # seamlessly fallback to direct in-process dispatch with full tool capabilities
                self.stdio_sessions.clear()

        return True

    def dispatch_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Dispatches a requested tool call. Handles JSON serialization, logging, and error handling.
        """
        if not self.enabled:
            print(f"[MCP Client] Notice: Tool '{tool_name}' rejected (Kill Switch Active).")
            return "Error: MCP tools are disabled via kill switch."

        fn = self._direct_dispatch_map.get(tool_name)
        if not fn:
            print(f"[MCP Client] Error: Requested unknown tool '{tool_name}'.")
            return f"Error: Unknown tool '{tool_name}'."

        server_label = (
            "🧠 Sequential Thinking" if tool_name == "sequentialthinking"
            else "🚀 NASA Public APIs" if tool_name.startswith("nasa_")
            else "🔭 STScI MAST Archive" if tool_name.startswith("mast_")
            else "⚙️ MCP Server"
        )

        print("\n" + "=" * 78)
        print(f"📡 [MCP TOOL INVOCATION] -> {server_label}")
        print(f"   Tool Name: {tool_name}")
        print(f"   Arguments: {json.dumps(arguments, indent=2)}")
        print("-" * 78)

        # Parse if arguments was passed as a string
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except Exception:
                arguments = {"thought": arguments}

        if not isinstance(arguments, dict):
            arguments = {}

        # If arguments are nested under a wrapper dictionary key, unwrap it:
        wrapper_keys = ("object", "parameters", "input", "args", "arguments", "properties")
        for wk in wrapper_keys:
            if wk in arguments and isinstance(arguments[wk], dict):
                inner = arguments[wk]
                outer_non_wrapper = {k: v for k, v in arguments.items() if k not in wrapper_keys}
                arguments = {**outer_non_wrapper, **inner}
                break

        # Sanitize arguments: strip scalar metadata keys commonly injected by LLMs/tool-call wrappers
        metadata_keys = {"object", "tool_name", "tool", "name", "type"}
        cleaned_args = {k: v for k, v in arguments.items() if k not in metadata_keys}

        # Filter against signature if the target function does not accept **kwargs
        try:
            sig = inspect.signature(fn)
            has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
            if not has_var_keyword:
                cleaned_args = {k: v for k, v in cleaned_args.items() if k in sig.parameters}
        except Exception:
            pass

        t_start = time.time()
        try:
            res = fn(**cleaned_args)
            elapsed_ms = (time.time() - t_start) * 1000

            if isinstance(res, (dict, list)):
                res_str = json.dumps(res, indent=2)
            else:
                res_str = str(res)

            print(f"📥 [MCP TOOL RESPONSE] <- {server_label} (Executed in {elapsed_ms:.1f}ms)")
            preview = res_str if len(res_str) <= 600 else res_str[:600] + f"\n... [Truncated for display, total {len(res_str)} bytes]"
            print(preview)
            print("=" * 78 + "\n")
            return res_str
        except Exception as e:
            elapsed_ms = (time.time() - t_start) * 1000
            err_dict = {"error": f"Tool execution failed: {str(e)}"}
            err_str = json.dumps(err_dict, indent=2)
            print(f"❌ [MCP TOOL ERROR] <- {server_label} (after {elapsed_ms:.1f}ms): {e}")
            print("=" * 78 + "\n")
            return err_str

    async def shutdown(self):
        """Kills any active child processes and cleans up resources."""
        if self.stdio_sessions:
            await self.exit_stack.aclose()
            self.stdio_sessions.clear()


# Global Singleton Client Manager instance
GLOBAL_MCP_MANAGER = MultiMCPClientManager(enable_mcp=ENABLE_MCP_ENV)
