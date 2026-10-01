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
        total_thoughts: int = 2,
        is_revision: Optional[bool] = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_thoughts: Optional[bool] = False,
        **kwargs
    ) -> Dict[str, Any]:
        # Cap planned thoughts to 2 for reliable reasoning without runaway context expansion
        effective_total = min(max(int(total_thoughts or 2), 1), 2)
        curr_step = int(thought_number or 1)

        if not thought:
            for alt_key in ("step", "reasoning", "analysis", "content", "query", "text"):
                if alt_key in kwargs:
                    thought = str(kwargs[alt_key])
                    break
            if not thought:
                thought = "Reasoning step registered."

        thought_entry = {
            "thought_number": curr_step,
            "total_thoughts": effective_total,
            "thought": thought,
            "is_revision": is_revision,
            "revises_thought": revises_thought,
            "branch_from_thought": branch_from_thought,
            "branch_id": branch_id
        }
        self.thoughts.append(thought_entry)
        
        # Enforce synthesis once step 2 or target is reached to avoid autoregressive looping
        if curr_step >= effective_total or curr_step >= 2:
            is_next_needed = False
            status = "READY_FOR_SYNTHESIS"
            feedback = f"Thought {curr_step}/{effective_total} registered. Plan complete. Proceed with final grounded synthesis now."
        else:
            is_next_needed = bool(next_thought_needed)
            status = "IN_PROGRESS" if is_next_needed else "READY_FOR_SYNTHESIS"
            feedback = (
                f"Thought {curr_step}/{effective_total} registered. "
                f"{'Continue reasoning steps.' if is_next_needed else 'Plan complete. Proceed with grounded synthesis.'}"
            )

        return {
            "status": status,
            "thought_number": curr_step,
            "total_thoughts_planned": effective_total,
            "history_length": len(self.thoughts),
            "feedback": feedback
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
