"""Portmanteau bumi(operation=...) — specs, OSS, optional HTTP bridge stub."""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx
from fastmcp import Context

from bumi_mcp.knowledge import (
    BUMI_HERO,
    MARKET_CONTEXT,
    NOETIX_GITHUB,
    OPENSOURCE_PAGE,
    VIRTUAL_TWIN_FLEET,
)

logger = logging.getLogger("bumi-mcp.portmanteau")


async def bumi_tool(
    ctx: Context | None = None,
    operation: str = "info",
) -> dict[str, Any]:
    """BUMI — Noetix Bumi humanoid: hero product info, OSS links, fleet virtual-twin map.

    PORTMANTEAU RATIONALE: Single entry for discovery and setup; hardware control arrives when
    a documented local API or ROS bridge is wired (set BUMI_ROBOT_URL for optional ping).

    Operations:
        info           — tagline + vendor + key specs (default)
        specs          — full structured hero dict
        sdk_links      — GitHub repos + opensource landing page
        robot_status   — if BUMI_ROBOT_URL set, GET {url}/health or /api/health; else connected=false
        virtual_twin   — how to drive virtual Bumi via resonite-mcp / robotics-mcp / worldlabs-mcp
        fleet_peers    — yahboom-mcp / dreame-mcp / robotics-mcp narrative for RoboFang fleet
        market         — Noetix story, China humbot wave, JD.com + tier-1 offline context (not legal advice)

    Returns:
        success, message, and operation-specific data.
    """
    correlation_id = getattr(ctx, "correlation_id", None) if ctx else None
    op = operation.lower().strip()
    logger.info("bumi(%s) correlation_id=%s", op, correlation_id)

    try:
        if op == "info":
            return {
                "success": True,
                "message": BUMI_HERO["tagline"],
                "product": BUMI_HERO["product"],
                "vendor": BUMI_HERO["vendor"],
                "specs_summary": BUMI_HERO["specs"],
                "retail_hint": (
                    "Consumer SKUs have listed on JD.com; tier-1 China cities combine app commerce with "
                    "walk-up electronics retail — see bumi(operation='market') for structured context."
                ),
            }

        if op == "specs":
            return {
                "success": True,
                "message": "Full Bumi hero profile + market context.",
                "data": {**BUMI_HERO, "market_context": MARKET_CONTEXT},
            }

        if op == "market":
            return {
                "success": True,
                "message": "Noetix positioning, China humbot landscape, JD + tier-1 retail context.",
                "data": MARKET_CONTEXT,
            }

        if op == "sdk_links":
            return {
                "success": True,
                "message": "Noetix public OSS entry points (verify license per repo).",
                "github": NOETIX_GITHUB,
                "opensource_page": OPENSOURCE_PAGE,
            }

        if op == "robot_status":
            return await _robot_status()

        if op == "virtual_twin":
            return {
                "success": True,
                "message": VIRTUAL_TWIN_FLEET["message"],
                "data": VIRTUAL_TWIN_FLEET,
            }

        if op == "fleet_peers":
            return {
                "success": True,
                "message": "Narrow robotics MCPs in the same fleet tier as bumi-mcp.",
                "peers": [
                    {
                        "id": "yahboom-mcp",
                        "note": "ROS 2 Raspbot — holonomic nav, patrol, agentic workflow.",
                    },
                    {
                        "id": "dreame-mcp",
                        "note": "DreameHome cloud vacuum — maps, clean cycles.",
                    },
                    {
                        "id": "robotics-mcp",
                        "note": "Composite hub — physical + virtual + noetix_info today.",
                    },
                ],
            }

        return {
            "success": False,
            "error": (
                f"Unknown operation: {operation}. "
                "Use: info, specs, sdk_links, market, robot_status, virtual_twin, fleet_peers."
            ),
        }
    except Exception as e:
        logger.exception("bumi(%s)", op)
        return {"success": False, "error": str(e), "error_type": type(e).__name__}


async def _robot_status() -> dict[str, Any]:
    base = (os.environ.get("BUMI_ROBOT_URL") or "").strip().rstrip("/")
    if not base:
        return {
            "success": True,
            "connected": False,
            "message": (
                "No BUMI_ROBOT_URL set. When a local bridge exposes HTTP, set e.g. "
                "BUMI_ROBOT_URL=http://192.168.1.50:8080 and robot_status will GET /health or /api/health."
            ),
        }
    for path in ("/health", "/api/health", "/status"):
        url = f"{base}{path}"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(url)
                if r.status_code < 500:
                    body: Any
                    try:
                        body = r.json()
                    except Exception:
                        body = r.text[:2000]
                    return {
                        "success": True,
                        "connected": r.status_code < 400,
                        "url": url,
                        "http_status": r.status_code,
                        "body": body,
                    }
        except Exception as e:
            logger.debug("robot_status %s failed: %s", url, e)
            continue
    return {
        "success": True,
        "connected": False,
        "message": f"Could not reach {base} on /health, /api/health, or /status.",
    }
