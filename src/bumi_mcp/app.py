"""FastAPI: REST dashboard + mounted MCP streamable HTTP."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bumi_mcp.config import load_settings
from bumi_mcp.knowledge import BUMI_HERO, VIRTUAL_TWIN_FLEET
from bumi_mcp.lifecycle import combined_lifespan
from bumi_mcp.server import mcp
from bumi_mcp.tools_manifest import MCP_TOOLS
from bumi_mcp.api_v1 import router as v1_router

mcp_http = mcp.http_app(path="/mcp")
router = APIRouter(prefix="/api")
llm_router = APIRouter(prefix="/api/llm")

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


@llm_router.get("/providers")
async def llm_providers() -> dict[str, Any]:
    providers: dict[str, Any] = {}
    async with httpx.AsyncClient(timeout=3) as c:
        try:
            r = await c.get("http://127.0.0.1:11434/api/tags")
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                providers["ollama"] = {"url": "http://127.0.0.1:11434", "models": models}
        except Exception:
            pass
        try:
            r = await c.get("http://127.0.0.1:1234/v1/models")
            if r.status_code == 200:
                models = [m["id"] for m in r.json().get("data", [])]
                providers["lm_studio"] = {"url": "http://127.0.0.1:1234", "models": models}
        except Exception:
            pass
    return {"providers": providers}


@llm_router.post("/chat")
async def llm_chat(body: dict[str, Any]) -> dict[str, Any]:
    provider = body.get("provider", "ollama")
    base_urls = {"ollama": "http://127.0.0.1:11434", "lm_studio": "http://127.0.0.1:1234"}
    base = base_urls.get(provider)
    if not base:
        return {"error": f"Unknown provider: {provider}"}
    messages = body.get("messages", [])
    model = body.get("model", "")
    payload = {"model": model, "messages": messages, "stream": False}
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{base}/v1/chat/completions", json=payload)
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def build_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(
        title="bumi-mcp",
        version="0.2.0",
        lifespan=combined_lifespan(mcp_http.lifespan),
    )
    _tauri = os.environ.get("BUMI_MCP_TAURI", "").lower() in ("1", "true", "yes")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:10774", "http://localhost:10774",
            "http://127.0.0.1:10775", "http://localhost:10775",
            "http://tauri.localhost", "https://tauri.localhost", "tauri://localhost",
        ],
        allow_origin_regex=r"https?://tauri\.localhost(:\d+)?" if _tauri else None,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    app.include_router(llm_router)
    app.include_router(v1_router)
    app.mount("/mcp", mcp_http)

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "service": "bumi-mcp",
            "version": "0.2.0",
            "mcp_http": f"http://{settings.host}:{settings.port}/mcp",
            "api": f"http://{settings.host}:{settings.port}/api",
            "webapp": "http://127.0.0.1:10775",
        }

    return app


app = build_app()
