"""FastAPI: REST dashboard + mounted MCP streamable HTTP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI

from bumi_mcp.config import load_settings
from bumi_mcp.knowledge import BUMI_HERO, VIRTUAL_TWIN_FLEET
from bumi_mcp.server import mcp
from bumi_mcp.tools_manifest import MCP_TOOLS

mcp_http = mcp.http_app(path="/mcp")
router = APIRouter(prefix="/api")

_FLEET_PATH = Path(__file__).resolve().parent / "data" / "fleet_default.json"


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "bumi-mcp"}


@router.get("/stats")
async def stats() -> dict[str, Any]:
    return {
        "product": BUMI_HERO["product"],
        "vendor": BUMI_HERO["vendor"],
        "dof": BUMI_HERO["specs"]["dof"],
        "virtual_twin_servers": len(VIRTUAL_TWIN_FLEET.get("mcp_servers", [])),
    }


@router.get("/hero")
async def hero() -> dict[str, Any]:
    return {"hero": BUMI_HERO, "virtual_twin": VIRTUAL_TWIN_FLEET}


@router.get("/tools")
async def tools() -> dict[str, Any]:
    return {"tools": MCP_TOOLS, "mcp_http_path": "/mcp"}


@router.get("/fleet")
async def fleet() -> dict[str, Any]:
    if _FLEET_PATH.is_file():
        hubs = json.loads(_FLEET_PATH.read_text(encoding="utf-8"))
    else:
        hubs = []
    return {"hubs": hubs}


def build_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(
        title="bumi-mcp",
        version="0.1.0",
        lifespan=mcp_http.lifespan,
    )
    app.include_router(router)
    app.mount("/mcp", mcp_http)

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "service": "bumi-mcp",
            "version": "0.1.0",
            "mcp_http": f"http://{settings.host}:{settings.port}/mcp",
            "api": f"http://{settings.host}:{settings.port}/api",
            "webapp": "http://127.0.0.1:10775",
        }

    return app


app = build_app()
