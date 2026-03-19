"""
LangGraph runtime provider for Hierarchy.

Tier 1 implementation: mechanical event loop that proves work can
flow from architect -> coordinator -> workers -> reviewer without
manual invocation at each step.

Usage:
    from corporeal.system.runtime.providers.langgraph import run_project

    result = run_project(
        brief="Build the portfolio dashboard",
        working_directory="C:/Users/AndrewBerman/Desktop/ajb_workspace/portal",
    )
"""

from .graph import build_graph, run_project

__all__ = ["build_graph", "run_project"]
