"""bumi portmanteau tests."""

from __future__ import annotations

import pytest

from bumi_mcp.portmanteau import bumi_tool


@pytest.mark.asyncio
async def test_bumi_info() -> None:
    r = await bumi_tool(ctx=None, operation="info")
    assert r["success"] is True
    assert r["product"] == "Noetix Bumi"


@pytest.mark.asyncio
async def test_bumi_unknown() -> None:
    r = await bumi_tool(ctx=None, operation="nope")
    assert r["success"] is False


@pytest.mark.asyncio
async def test_bumi_market() -> None:
    r = await bumi_tool(ctx=None, operation="market")
    assert r["success"] is True
    assert "china_humbot_explosion" in r["data"]


@pytest.mark.asyncio
async def test_robot_status_no_url() -> None:
    r = await bumi_tool(ctx=None, operation="robot_status")
    assert r["success"] is True
    assert r.get("connected") is False
