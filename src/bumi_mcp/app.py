"""FastAPI: REST dashboard + mounted MCP streamable HTTP."""

from __future__ import annotations

import json
import os
import time
from collections import deque
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx
from fastapi import APIRouter, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response

from bumi_mcp.config import load_settings
from bumi_mcp.knowledge import BUMI_HERO, VIRTUAL_TWIN_FLEET
from bumi_mcp.lifecycle import combined_lifespan
from bumi_mcp.server import mcp
from bumi_mcp.tools_manifest import MCP_TOOLS
from bumi_mcp.api_v1 import router as v1_router

mcp_http = mcp.http_app(path="/mcp")
router = APIRouter(prefix="/api")
llm_router = APIRouter(prefix="/api/llm")


# ── Ring-buffer activity log ──────────────────────────────────────────

class ActivityLog:
    def __init__(self, max_entries: int = 2000):
        self.max_entries = max_entries
        self._entries: deque[dict[str, Any]] = deque(maxlen=max_entries)

    def add(self, level: str, kind: str, detail: str, meta: dict | None = None) -> str:
        entry_id = f"{time.time():.6f}.{uuid4().hex[:6]}"
        self._entries.append({
            "id": entry_id, "level": level.upper(), "kind": kind, "detail": detail, "meta": meta or {},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + f".{int(time.time()*1e6)%1000000:06d}Z",
        })
        return entry_id

    def query(self, limit=50, offset=0, level=None, kind=None, search=None, sort="desc", after_id=None) -> dict:
        entries = list(self._entries)
        if after_id:
            try:
                after_time = float(after_id.split(".")[0])
                entries = [e for e in entries if float(e["id"].split(".")[0]) > after_time]
            except (ValueError, IndexError): pass
        if level:
            lvls = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
            min_lvl = lvls.get(level.upper(), 1)
            entries = [e for e in entries if lvls.get(e["level"], 1) >= min_lvl]
        if kind: entries = [e for e in entries if e["kind"] == kind]
        if search:
            q = search.lower()
            entries = [e for e in entries if q in e["detail"].lower()]
        entries.sort(key=lambda e: e["id"], reverse=(sort == "desc"))
        total = len(entries)
        return {"entries": entries[offset:offset + limit], "total": total, "limit": limit, "offset": offset, "max_entries": self.max_entries, "sort": sort}

    def stats(self) -> dict:
        levels, kinds = {}, {}
        for e in self._entries:
            levels[e["level"]] = levels.get(e["level"], 0) + 1
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        return {"total": len(self._entries), "max_entries": self.max_entries, "levels": levels, "kinds": kinds}

    def clear(self): self._entries.clear()

activity_log = ActivityLog()


# ── Logging routes ────────────────────────────────────────────────────

log_router = APIRouter(prefix="/api/logs")

@log_router.get("")
async def get_logs(request: Request, limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0),
                   level: str | None = Query(None), kind: str | None = Query(None),
                   search: str | None = Query(None), sort: str = Query("desc", regex="^(asc|desc)$"),
                   after_id: str | None = Query(None)):
    return activity_log.query(limit=limit, offset=offset, level=level, kind=kind, search=search, sort=sort, after_id=after_id)

@log_router.get("/stats")
async def logs_stats(): return activity_log.stats()

@log_router.get("/export")
async def logs_export(format: str = Query("json", regex="^(json|csv)$"), level: str | None = Query(None),
                     kind: str | None = Query(None), search: str | None = Query(None)):
    return PlainTextResponse("[]", media_type="application/json")

@log_router.delete("")
async def clear_logs(): activity_log.clear(); return {"success": True, "message": "Logs cleared."}

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
    app.include_router(log_router)
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
