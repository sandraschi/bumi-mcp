# bumi-mcp — Agent Guide

## Overview
FastMCP 3.1.0 MCP for Noetix Bumi humanoid — hero specs, OSS links, fleet virtual-twin guidance, optional robot bridge

## Entry Points

- `uv run bumi-mcp` → `bumi_mcp.__main__:main`
- `just serve` → FastAPI :10774 + `/api/v1/*` + MCP `/mcp`

## Standards
- FastMCP 3.2+ portmanteau tool pattern — tools use `operation` enum param
- Responses: structured dicts with `success`, `message`, domain-specific fields
- Dual transport: stdio (Claude Desktop) + HTTP (`MCP_TRANSPORT=http`)
- See [mcp-central-docs](https://github.com/sandraschi/mcp-central-docs) for fleet-wide coding standards

## Key Files
- `README.md` — full documentation
- `STATUS.md` / `INTEGRATION.md` — physical bot readiness
- `pyproject.toml` — build config and entry points
- `CLAUDE.md` — Claude Code context (if present)

## Quick Ref

```powershell
uv run pytest tests/ -q
just ci
```

Install docs: follow mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md
