"""FastAPI lifespan: MCP + optional robot bridge."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from bumi_mcp.bridge_factory import create_bridge
from bumi_mcp.bridge_state import set_bridge
from bumi_mcp.config import load_settings

logger = logging.getLogger("bumi-mcp.lifecycle")


@asynccontextmanager
async def bridge_lifespan(_app: FastAPI):
    settings = load_settings()
    bridge = create_bridge(settings)
    set_bridge(bridge)

    connect_task: asyncio.Task[None] | None = None

    async def _connect() -> None:
        ok = await bridge.connect(timeout=settings.connect_timeout_s)
        if ok:
            logger.info("Robot bridge ready (mock=%s)", settings.use_mock_bridge)
        else:
            logger.warning(
                "Robot bridge offline — set BUMI_IP + rosbridge on Jetson, or BUMI_USE_MOCK_BRIDGE=1 for dev"
            )

    if settings.use_mock_bridge or settings.robot_ip:
        connect_task = asyncio.create_task(_connect())

    try:
        yield
    finally:
        logger.info("Shutting down robot bridge")
        if connect_task and not connect_task.done():
            connect_task.cancel()
        await bridge.disconnect()
        set_bridge(None)


def combined_lifespan(mcp_lifespan):
    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        async with mcp_lifespan(app):
            async with bridge_lifespan(app):
                yield

    return _lifespan
