"""
================================================================================
MCP Server: Sequential Thinking
Specialization: Dynamic Multi-Step Reasoning, Hypothesis Testing, & Verification
================================================================================
"""

import json
from typing import Dict, Any, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False

class SequentialThinkingTracker:
    """Manages internal thought traces, revisions, and branching for complex reasoning."""
    def __init__(self):
        self.thoughts: List[Dict[str, Any]] = []
        self.branches: Dict[str, List[Dict[str, Any]]] = {}

    def process_thought(
        self,
        thought: str = "",
        next_thought_needed: bool = True,
        thought_number: int = 1,
        total_thoughts: int = 3,
        is_revision: Optional[bool] = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_thoughts: Optional[bool] = False,
        **kwargs
    ) -> Dict[str, Any]:
        if not thought:
            for alt_key in ("step", "reasoning", "analysis", "content", "query", "text"):
                if alt_key in kwargs:
                    thought = str(kwargs[alt_key])
                    break
            if not thought:
                thought = "Reasoning step registered."

        thought_entry = {
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "thought": thought,
            "is_revision": is_revision,
            "revises_thought": revises_thought,
            "branch_from_thought": branch_from_thought,
            "branch_id": branch_id
        }
        self.thoughts.append(thought_entry)
        
        status = "IN_PROGRESS" if next_thought_needed else "READY_FOR_SYNTHESIS"
        if needs_more_thoughts:
            status = "EXPANDING_PLAN"

        return {
            "status": status,
            "thought_number": thought_number,
            "total_thoughts_planned": total_thoughts,
            "history_length": len(self.thoughts),
            "feedback": (
                f"Thought {thought_number}/{total_thoughts} registered. "
                f"{'Continue reasoning steps.' if next_thought_needed else 'Plan complete. Proceed with grounded synthesis.'}"
            )
        }

    def reset(self):
        self.thoughts.clear()
        self.branches.clear()

GLOBAL_TRACKER = SequentialThinkingTracker()

def sequential_thinking(
    thought: str = "",
    next_thought_needed: bool = True,
    thought_number: int = 1,
    total_thoughts: int = 3,
    is_revision: Optional[bool] = False,
    revises_thought: Optional[int] = None,
    branch_from_thought: Optional[int] = None,
    branch_id: Optional[str] = None,
    needs_more_thoughts: Optional[bool] = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Executes a structured reasoning step. Allows decomposing complex NASA space
    queries, evaluating evidence, revising assumptions, and structuring multi-hop analyses.
    """
    return GLOBAL_TRACKER.process_thought(
        thought=thought,
        next_thought_needed=next_thought_needed,
        thought_number=thought_number,
        total_thoughts=total_thoughts,
        is_revision=is_revision,
        revises_thought=revises_thought,
        branch_from_thought=branch_from_thought,
        branch_id=branch_id,
        needs_more_thoughts=needs_more_thoughts,
        **kwargs
    )

SEQUENTIAL_THINKING_TOOLS = {
    "sequentialthinking": sequential_thinking
}

if FASTMCP_AVAILABLE:
    mcp = FastMCP("Sequential-Thinking-Server")

    @mcp.tool()
    def sequentialthinking(
        thought: str = "",
        next_thought_needed: bool = True,
        thought_number: int = 1,
        total_thoughts: int = 3,
        is_revision: Optional[bool] = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_thoughts: Optional[bool] = False,
        **kwargs
    ) -> dict:
        """Executes a structured reasoning step for complex query decomposition."""
        return sequential_thinking(
            thought=thought,
            next_thought_needed=next_thought_needed,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts,
            **kwargs
        )

if __name__ == "__main__":
    if FASTMCP_AVAILABLE:
        mcp.run()
    else:
        print("Sequential Thinking MCP Server loaded in standalone mode.")
