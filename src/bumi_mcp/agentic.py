"""SEP-1577 agentic workflow — plan against Bumi + fleet context."""

from __future__ import annotations

import logging

from fastmcp import Context

from bumi_mcp.portmanteau import bumi_tool

logger = logging.getLogger("bumi-mcp.agentic")


async def bumi_agentic_workflow(goal: str, ctx: Context) -> str:
    """BUMI_AGENTIC_WORKFLOW — High-level goals: specs, SDK setup, virtual twin, fleet composition.

    Uses ctx.sample() so the host LLM can call bumi_tool and sibling MCPs (resonite, robotics).

    Args:
        goal: Natural language, e.g. "Summarize Bumi specs and how to show a virtual twin in Resonite"

    Returns:
        LLM summary string.
    """
    snap_parts: list[str] = []
    for op in ("info", "market", "sdk_links", "virtual_twin"):
        try:
            r = await bumi_tool(ctx=ctx, operation=op)
            if r.get("success"):
                snap_parts.append(f"{op}: {r.get('message', '')[:200]}")
        except Exception:
            snap_parts.append(f"{op}: unavailable")

    snapshot = "\n".join(snap_parts)

    prompt = (
        f"Context snapshot from bumi_mcp:\n{snapshot}\n\n"
        f"User goal: {goal}\n\n"
        "Available tool: bumi(operation=...) with "
        "info | specs | sdk_links | robot_status | virtual_twin | fleet_peers.\n"
        "For vbot / virtual worlds, compose robotics-mcp, resonite-mcp, unity3d-mcp, "
        "blender-mcp, worldlabs-mcp — bumi-mcp does not replace those servers.\n\n"
        "Plan concise next steps and risks (safety for physical motion). Summarize."
    )

    try:
        result = await ctx.sample(prompt)
        return result.text if hasattr(result, "text") else str(result)
    except Exception as e:
        logger.exception("bumi_agentic_workflow sampling failed")
        return f"Workflow failed (sampling unavailable in this client?): {e}"
