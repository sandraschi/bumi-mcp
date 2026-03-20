# bumi-mcp — just recipes (https://github.com/casey/just)

default:
    @just --list

serve:
    uv run python -m bumi_mcp --serve

stdio:
    uv run python -m bumi_mcp --stdio

test:
    uv run pytest -q

lint:
    uv run ruff check .
    uv run ruff format --check .

fmt:
    uv run ruff format .
    uv run ruff check --fix .
