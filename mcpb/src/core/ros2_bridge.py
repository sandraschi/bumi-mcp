"""Slim rosbridge client for Noetix Bumi — telemetry first, gated motion."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any

import roslibpy

logger = logging.getLogger("bumi-mcp.core.ros2_bridge")

# Placeholder joint names until vendor SDK docs confirm naming.
_BUMI_JOINT_NAMES = [
    "left_hip_pitch",
    "left_hip_roll",
    "left_knee",
    "left_ankle_pitch",
    "left_ankle_roll",
    "left_toe",
    "right_hip_pitch",
    "right_hip_roll",
    "right_knee",
    "right_ankle_pitch",
    "right_ankle_roll",
    "right_toe",
    "lumbar",
    "left_shoulder",
    "left_elbow",
    "left_wrist",
    "right_shoulder",
    "right_elbow",
    "right_wrist",
    "head_yaw",
    "head_pitch",
]


class BumiROS2Bridge:
    """Humanoid-safe rosbridge wrapper. Motion requires BUMI_ALLOW_MOTION=1."""

    skip_video_bridge = True

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9090,
        fallback_host: str | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.fallback_host = fallback_host
        self.ros: roslibpy.Ros | None = None
        self.connected = False
        self.motion_allowed = (os.environ.get("BUMI_ALLOW_MOTION") or "").strip().lower() in (
            "1",
            "true",
            "yes",
            "on",
        )
        self.imu_topic = (os.environ.get("BUMI_IMU_TOPIC") or "/imu/data").strip()
        self.battery_topic = (os.environ.get("BUMI_BATTERY_TOPIC") or "/battery_state").strip()
        self.joint_states_topic = (os.environ.get("BUMI_JOINT_STATES_TOPIC") or "/joint_states").strip()
        self.walk_cmd_topic = (os.environ.get("BUMI_WALK_CMD_TOPIC") or "").strip()
        self.estop_topic = (os.environ.get("BUMI_ESTOP_TOPIC") or "").strip()
        self.state: dict[str, Any] = {
            "imu": {},
            "battery": {},
            "joint_states": {"names": [], "positions": []},
            "mode": "unknown",
            "last_update": 0.0,
        }
        self._listeners: list[roslibpy.Topic] = []
        self._walk_publisher: roslibpy.Topic | None = None
        self._estop_publisher: roslibpy.Topic | None = None

    async def connect(self, timeout: float = 15.0) -> bool:
        if self.ros and self.ros.is_connected:
            return True

        host = self.host
        if self.fallback_host and not await self._tcp_reachable(host, self.port):
            host = self.fallback_host

        self.ros = roslibpy.Ros(host=host, port=self.port)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.ros.run)

        deadline = time.time() + min(timeout, 8.0)
        while self.ros and not self.ros.is_connected and time.time() < deadline:
            await asyncio.sleep(0.25)

        if not self.ros or not self.ros.is_connected:
            self.connected = False
            logger.warning("BumiROS2Bridge: handshake failed at %s:%s", host, self.port)
            return False

        self.host = host
        self.connected = True
        self._subscribe_topics()
        logger.info("BumiROS2Bridge connected at %s:%s", host, self.port)
        return True

    async def disconnect(self) -> None:
        for listener in self._listeners:
            try:
                listener.unsubscribe()
            except Exception:
                pass
        self._listeners.clear()
        self._walk_publisher = None
        self._estop_publisher = None
        if self.ros and self.ros.is_connected:
            try:
                self.ros.close()
            except Exception:
                logger.debug("ros close", exc_info=True)
        self.ros = None
        self.connected = False

    async def _tcp_reachable(self, host: str, port: int, timeout: float = 0.8) -> bool:
        try:
            _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        except (TimeoutError, OSError, ConnectionError):
            return False
        else:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return True

    def _subscribe_topics(self) -> None:
        assert self.ros is not None

        def _imu_cb(msg: dict[str, Any]) -> None:
            ori = msg.get("orientation") or {}
            self.state["imu"] = {
                "orientation": ori,
                "angular_velocity": msg.get("angular_velocity") or {},
                "linear_acceleration": msg.get("linear_acceleration") or {},
            }
            self.state["last_update"] = time.time()

        def _battery_cb(msg: dict[str, Any]) -> None:
            pct = msg.get("percentage")
            if pct is not None and pct <= 1.0:
                pct = round(float(pct) * 100.0, 1)
            self.state["battery"] = {
                "percentage": pct,
                "voltage": msg.get("voltage"),
                "power_supply_status": msg.get("power_supply_status"),
            }
            self.state["last_update"] = time.time()

        def _joint_cb(msg: dict[str, Any]) -> None:
            self.state["joint_states"] = {
                "names": list(msg.get("name") or []),
                "positions": list(msg.get("position") or []),
            }
            self.state["last_update"] = time.time()

        for topic, msg_type, cb in (
            (self.imu_topic, "sensor_msgs/msg/Imu", _imu_cb),
            (self.battery_topic, "sensor_msgs/msg/BatteryState", _battery_cb),
            (self.joint_states_topic, "sensor_msgs/msg/JointState", _joint_cb),
        ):
            listener = roslibpy.Topic(self.ros, topic, msg_type)
            listener.subscribe(cb)
            self._listeners.append(listener)

        if self.walk_cmd_topic and self.motion_allowed:
            self._walk_publisher = roslibpy.Topic(
                self.ros,
                self.walk_cmd_topic,
                "geometry_msgs/msg/TwistStamped",
            )
            self._walk_publisher.advertise()

        if self.estop_topic:
            self._estop_publisher = roslibpy.Topic(self.ros, self.estop_topic, "std_msgs/msg/Bool")
            self._estop_publisher.advertise()

    def get_full_telemetry(self) -> dict[str, Any]:
        battery = self.state.get("battery") or {}
        joints = self.state.get("joint_states") or {}
        return {
            "robot": "noetix_bumi",
            "mode": self.state.get("mode", "unknown"),
            "battery_pct": battery.get("percentage"),
            "voltage": battery.get("voltage"),
            "imu": self.state.get("imu") or {},
            "joint_states": joints,
            "joint_count": len(joints.get("names") or []),
            "expected_dof": 21,
            "last_update": self.state.get("last_update"),
            "motion_allowed": self.motion_allowed,
            "walk_cmd_topic": self.walk_cmd_topic or None,
        }

    async def estop(self) -> bool:
        if not self.connected:
            return False
        if self._estop_publisher:
            self._estop_publisher.publish({"data": True})
            self.state["mode"] = "estop"
            return True
        if self._walk_publisher:
            self._walk_publisher.publish(
                {
                    "header": {"frame_id": "base_link"},
                    "twist": {
                        "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "angular": {"x": 0.0, "y": 0.0, "z": 0.0},
                    },
                }
            )
            self.state["mode"] = "estop"
            return True
        logger.warning("estop: no BUMI_ESTOP_TOPIC or BUMI_WALK_CMD_TOPIC configured")
        return False

    async def walk(self, linear_x: float = 0.0, angular_z: float = 0.0) -> bool:
        if not self.motion_allowed:
            logger.warning("walk rejected: set BUMI_ALLOW_MOTION=1 after SDK validation")
            return False
        if not self.connected or not self._walk_publisher:
            return False
        self._walk_publisher.publish(
            {
                "header": {"frame_id": "base_link"},
                "twist": {
                    "linear": {"x": linear_x, "y": 0.0, "z": 0.0},
                    "angular": {"x": 0.0, "y": 0.0, "z": angular_z},
                },
            }
        )
        self.state["mode"] = "walking" if abs(linear_x) + abs(angular_z) > 1e-4 else "standing"
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
        return False

    def placeholder_joint_names(self) -> list[str]:
        return list(_BUMI_JOINT_NAMES)
