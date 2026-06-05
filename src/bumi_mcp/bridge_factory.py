"""Create ROS or mock bridge from settings."""

from __future__ import annotations

import logging
from typing import Any

from bumi_mcp.config import Settings

logger = logging.getLogger("bumi-mcp.bridge_factory")


def create_bridge(settings: Settings) -> Any:
    if settings.use_mock_bridge:
        from bumi_mcp.testing.mock_bridge import MockBumiBridge

        logger.info("Using MockBumiBridge (BUMI_USE_MOCK_BRIDGE=1)")
        return MockBumiBridge(host=settings.robot_ip, port=settings.bridge_port)

    try:
        from bumi_mcp.core.ros2_bridge import BumiROS2Bridge
    except ImportError as exc:
        logger.warning("roslibpy unavailable (%s); falling back to mock bridge", exc)
        from bumi_mcp.testing.mock_bridge import MockBumiBridge

        return MockBumiBridge(host=settings.robot_ip, port=settings.bridge_port)

    logger.info("Using BumiROS2Bridge → %s:%s", settings.robot_ip, settings.bridge_port)
    return BumiROS2Bridge(
        host=settings.robot_ip,
        port=settings.bridge_port,
        fallback_host=settings.fallback_ip,
    )
