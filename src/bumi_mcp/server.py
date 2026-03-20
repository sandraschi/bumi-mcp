"""FastMCP 3.1 — Noetix Bumi humanoid MCP."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider

from bumi_mcp.agentic import bumi_agentic_workflow
from bumi_mcp.portmanteau import bumi_tool

mcp = FastMCP(
    "bumi-mcp",
    instructions=(
        "Noetix Bumi humanoid (hero consumer robot): use bumi(operation=...) for specs, "
        "OSS/SDK links, optional BUMI_ROBOT_URL health ping, and virtual_twin fleet map. "
        "Physical motion control belongs behind vendor SDK / ROS — not implied here until wired."
    ),
)

_skills = Path(__file__).resolve().parent / "skills"
if _skills.is_dir():
    mcp.add_provider(SkillsDirectoryProvider(roots=[_skills]))

mcp.tool()(bumi_tool)
mcp.tool()(bumi_agentic_workflow)


@mcp.prompt(
    name="bumi_quick_start",
    description="Operator brief: Bumi specs, OSS repos, and virtual twin via fleet MCPs.",
    tags={"noetix", "bumi", "robotics", "fleet"},
)
def bumi_quick_start(
    focus: Literal["physical", "virtual", "fleet"] = "fleet",
) -> str:
    """Return a reusable system-style brief for agents working with Bumi."""
    base = (
        "You are assisting with Noetix Bumi, a compact consumer humanoid (ROS/Linux SDKs). "
        "Call bumi(operation='specs'|'sdk_links'|'info') for facts. "
        "Never claim direct motor control unless a verified bridge is configured (BUMI_ROBOT_URL).\n"
    )
    if focus == "physical":
        return (
            base + "\nFocus physical: verify battery, workspace clearance, e-stop, "
            "and vendor safety docs before any motion. Prefer small scripted poses when SDK allows."
        )
    if focus == "virtual":
        return (
            base + "\nFocus virtual: use bumi(operation='virtual_twin'). "
            "Actual Resonite/world driving is via resonite-mcp and robotics-mcp — compose, don't duplicate."
        )
    return (
        base
        + "\nFocus fleet: bumi(operation='fleet_peers') for yahboom/dreame/robotics-mcp context. "
        "Orchestrate multi-server workflows explicitly in the tool plan."
    )
