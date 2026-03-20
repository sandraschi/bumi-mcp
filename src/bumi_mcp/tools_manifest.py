"""Static MCP tool catalog for dashboard / fleet."""

from __future__ import annotations

from typing import Any

MCP_TOOLS: list[dict[str, Any]] = [
    {
        "name": "bumi",
        "description": "Noetix Bumi — info, specs, sdk_links, market, robot_status, virtual_twin, fleet_peers.",
        "params": {"operation": "str"},
    },
    {
        "name": "bumi_agentic_workflow",
        "description": "LLM-planned goals over Bumi + fleet (SEP-1577 sampling).",
        "params": {"goal": "str"},
    },
    {
        "name": "bumi_quick_start",
        "kind": "prompt",
        "description": "MCP prompt — operator brief for Bumi + virtual twin composition.",
        "params": {"focus": "physical|virtual|fleet"},
    },
]
