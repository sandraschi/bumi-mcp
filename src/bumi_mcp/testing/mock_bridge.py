"""In-memory Bumi bridge for CI and teleoperator contract testing."""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("bumi-mcp.testing.mock_bridge")


class _MockRosConn:
    __slots__ = ("_bridge",)

    def __init__(self, bridge: MockBumiBridge) -> None:
        self._bridge = bridge

    @property
    def is_connected(self) -> bool:
        return self._bridge.connected


class MockBumiBridge:
    """Mirrors BumiROS2Bridge surface used by /api/v1 and future BumiAdapter."""

    skip_video_bridge = True

    def __init__(self, host: str = "127.0.0.1", port: int = 9090) -> None:
        self.host = host
        self.port = port
        self.ros = _MockRosConn(self)
        self.connected = False
        self.motion_allowed = True
        self.walk_history: list[dict[str, float]] = []
        self.estop_count = 0
        self.state: dict[str, Any] = {
            "mode": "standing",
            "imu": {
                "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
                "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
                "linear_acceleration": {"x": 0.0, "y": 0.0, "z": 9.81},
            },
            "battery": {"percentage": 92.0, "voltage": 48.2, "power_supply_status": 2},
            "joint_states": {
                "names": [
                    "left_hip_pitch",
                    "left_knee",
                    "right_hip_pitch",
                    "right_knee",
                    "lumbar",
                    "head_yaw",
                    "head_pitch",
                ],
                "positions": [0.01, -0.02, 0.01, -0.02, 0.0, 0.0, -0.05],
            },
            "last_update": 0.0,
        }

    async def connect(self, timeout: float = 10.0) -> bool:
        self.connected = True
        self.state["last_update"] = time.time()
        logger.info("MockBumiBridge: connected (no network)")
        return True

    async def disconnect(self) -> None:
        self.connected = False
        logger.info("MockBumiBridge: disconnected")

    def get_full_telemetry(self) -> dict[str, Any]:
        battery = self.state.get("battery") or {}
        joints = self.state.get("joint_states") or {}
        return {
            "robot": "noetix_bumi",
            "mode": self.state.get("mode", "standing"),
            "battery_pct": battery.get("percentage"),
            "voltage": battery.get("voltage"),
            "imu": self.state.get("imu") or {},
            "joint_states": joints,
            "joint_count": len(joints.get("names") or []),
            "expected_dof": 21,
            "last_update": self.state.get("last_update"),
            "motion_allowed": self.motion_allowed,
            "walk_cmd_topic": "/bumi/walk_cmd (mock)",
        }

    async def estop(self) -> bool:
        if not self.connected:
            return False
        self.estop_count += 1
        self.state["mode"] = "estop"
        self.walk_history.clear()
        return True

    async def walk(self, linear_x: float = 0.0, angular_z: float = 0.0) -> bool:
        if not self.connected or not self.motion_allowed:
            return False
        self.walk_history.append({"linear_x": linear_x, "angular_z": angular_z})
        self.state["mode"] = "walking" if abs(linear_x) + abs(angular_z) > 1e-4 else "standing"
        self.state["last_update"] = time.time()
        return True

    async def set_head(self, yaw_deg: float, pitch_deg: float) -> bool:
        if not self.connected:
            return False
        self.state["head_target"] = {"yaw_deg": yaw_deg, "pitch_deg": pitch_deg}
        self.state["last_update"] = time.time()
        return True

    async def set_manip_target(self, payload: dict[str, Any]) -> bool:
        if not self.connected:
            return False
        self.state["manip_target"] = payload
        self.state["last_update"] = time.time()
        return True

    def placeholder_joint_names(self) -> list[str]:
        return list(self.state["joint_states"]["names"])
