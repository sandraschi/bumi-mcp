"""CLI: stdio (Cursor) or HTTP (FastAPI + /mcp)."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys

import uvicorn

from bumi_mcp.config import load_settings
from bumi_mcp.server import mcp


def _configure_logging(*, debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="bumi-mcp (FastMCP 3.1)")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Run FastAPI on BUMI_MCP_HOST:BUMI_MCP_PORT with MCP at /mcp",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="MCP stdio only (default if --serve not passed)",
    )
    parser.add_argument("--debug", action="store_true", help="Verbose stderr logs")
    args = parser.parse_args()
    _configure_logging(debug=args.debug)

    transport = os.getenv("MCP_TRANSPORT", "").lower()
    use_http = args.serve or transport in {"http", "streamable"}

    if use_http and args.stdio:
        parser.error("Choose either --serve or --stdio, not both.")

    if use_http:
        s = load_settings()
        uvicorn.run(
            "bumi_mcp.app:app",
            host=s.host,
            port=s.port,
            log_level="debug" if args.debug else "info",
        )
        return

    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
