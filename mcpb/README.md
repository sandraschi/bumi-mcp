# Bumi MCP (MCPB Bundle)

MCP server for the Noetix Bumi humanoid robot.

## Usage

```json
{
  "mcpServers": {
    "bumi": {
      "command": "uv",
      "args": ["run", "--directory", "${PWD}", "python", "-m", "bumi_mcp", "--stdio"],
      "env": { "PYTHONPATH": "${PWD}/src" }
    }
  }
}
```

## Tools

- **bumi** — product info, specs, SDK links, market analysis, robot status, telemetry, virtual twin fleet map, fleet peers
- **bumi_agentic_workflow** — LLM-planned multi-step research goals

## Requirements

- Python 3.12+
- uv
