"""Process-wide bridge handle for FastAPI routes and MCP tools."""

from __future__ import annotations

from typing import Any

_state: dict[str, Any] = {}


def get_bridge() -> Any | None:
    return _state.get("bridge")


def set_bridge(bridge: Any | None) -> None:
    _state["bridge"] = bridge
