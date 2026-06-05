"""REST v1 — teleoperator-mcp / fleet contract (health, telemetry, gated control)."""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from bumi_mcp.bridge_state import get_bridge
from bumi_mcp.testing.mock_bridge import MockBumiBridge

router = APIRouter(prefix="/api/v1")
_start_time = time.time()


class ManipCommand(BaseModel):
    """WebXR hand skeleton or controller grip fallback — SDK mapping TBD."""

    source: str = "unknown"
    left: dict[str, Any] | None = None
    right: dict[str, Any] | None = None
    left_grip: float | None = Field(default=None, ge=0.0, le=1.0)
    right_grip: float | None = Field(default=None, ge=0.0, le=1.0)


@router.get("/health")
async def health_v1() -> dict[str, Any]:
    bridge = get_bridge()
    connected = bool(bridge and bridge.connected)
    ros_connected = False
    if bridge and getattr(bridge, "ros", None):
        ros_connected = bool(bridge.ros.is_connected)

    return {
        "status": "online",
        "service": "bumi-mcp",
        "robot": "noetix_bumi",
        "connected": connected,
        "ros_connected": ros_connected,
        "mock": isinstance(bridge, MockBumiBridge),
        "mode": (bridge.state.get("mode") if bridge else None) or "offline",
        "motion_allowed": bool(getattr(bridge, "motion_allowed", False)) if bridge else False,
        "uptime_s": round(time.time() - _start_time, 1),
    }


@router.get("/telemetry")
async def telemetry_v1() -> dict[str, Any]:
    bridge = get_bridge()
    if not bridge or not bridge.connected:
        raise HTTPException(status_code=503, detail="Robot bridge offline")
    return {"success": True, "telemetry": bridge.get_full_telemetry()}


@router.post("/control/estop")
async def estop_v1() -> dict[str, Any]:
    bridge = get_bridge()
    if not bridge:
        raise HTTPException(status_code=503, detail="Bridge not initialized")
    ok = await bridge.estop()
    if not ok:
        raise HTTPException(status_code=503, detail="E-stop failed (bridge offline or topic unset)")
    return {"success": True, "message": "E-stop sent", "mode": bridge.state.get("mode")}


@router.post("/control/walk")
async def walk_v1(
    linear: float = Query(0.0, ge=-1.0, le=1.0),
    angular: float = Query(0.0, ge=-1.0, le=1.0),
) -> dict[str, Any]:
    bridge = get_bridge()
    if not bridge or not bridge.connected:
        raise HTTPException(status_code=503, detail="Robot bridge offline")
    ok = await bridge.walk(linear_x=linear, angular_z=angular)
    if not ok:
        raise HTTPException(
            status_code=403,
            detail="Walk rejected — enable BUMI_ALLOW_MOTION=1 and configure BUMI_WALK_CMD_TOPIC on hardware",
        )
    return {"success": True, "linear": linear, "angular": angular}


@router.post("/control/head")
async def head_v1(
    yaw: float = Query(0.0, ge=-90.0, le=90.0),
    pitch: float = Query(0.0, ge=-45.0, le=45.0),
) -> dict[str, Any]:
    bridge = get_bridge()
    if not bridge or not bridge.connected:
        raise HTTPException(status_code=503, detail="Robot bridge offline")
    ok = await bridge.set_head(yaw, pitch)
    return {
        "success": ok,
        "message": "Head command accepted (mock)" if ok else "Head control not wired to SDK yet",
        "yaw": yaw,
        "pitch": pitch,
    }


@router.post("/control/manip")
async def manip_v1(body: ManipCommand) -> dict[str, Any]:
    bridge = get_bridge()
    if not bridge or not bridge.connected:
        raise HTTPException(status_code=503, detail="Robot bridge offline")
    stored = await bridge.set_manip_target(body.model_dump(exclude_none=True))
    return {
        "success": stored,
        "message": "Manip target stored (mock)" if stored else "Arm SDK not wired on hardware yet",
        "payload": body.model_dump(exclude_none=True),
    }
