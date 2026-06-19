set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
import 'scripts/just/fleet.just'

# ── Dashboard ─────────────────────────────────────────────────────────────────

# Open the interactive recipe dashboard in the browser
default:
    @just --list

# ── Quality ───────────────────────────────────────────────────────────────────

# Execute Ruff SOTA v13.1 linting
lint:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check .
    Set-Location '{{justfile_directory()}}\web_sota'
    npx @biomejs/biome ci .

# Execute Ruff SOTA v13.1 fix and formatting
fix:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check . --fix --unsafe-fixes
    uv run ruff format .
    Set-Location '{{justfile_directory()}}\web_sota'
    npx @biomejs/biome check --write .

# ── Hardening ─────────────────────────────────────────────────────────────────

# Execute Bandit security audit
check-sec:
    Set-Location '{{justfile_directory()}}'
    uv run bandit -r src/

# Execute safety audit of dependencies
audit-deps:
    Set-Location '{{justfile_directory()}}'
    uv run safety check

# bumi-mcp — just recipes (https://github.com/casey/just)

stats:
    uv run python tools/repo_stats.py

serve:
    uv run python -m bumi_mcp --serve

stdio:
    uv run python -m bumi_mcp --stdio

test:
    uv run pytest -q

ci:
    uv sync --all-extras
    uv run pytest -q

fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Bundle for Claude Desktop (MCPB)
mcpb-pack:
    mkdir -p mcpb/src
    Copy-Item src\\bumi_mcp mcpb\\src\\ -Recurse -Force
    Remove-Item mcpb\\src\\bumi_mcp\\__pycache__ -Recurse -Force -ErrorAction SilentlyContinue
    mcpb pack mcpb dist\\bumi-mcp-v0.2.0.mcpb
