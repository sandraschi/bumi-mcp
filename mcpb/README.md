# bumi-mcp (MCPB Bundle)

FastMCP 3.1.0 MCP for Noetix Bumi humanoid — hero specs, OSS links, fleet virtual-twin guidance, optional robot bridge

## Usage

Add to \claude_desktop_config.json\:
\\\json
{
  "mcpServers": {
    "bumi-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "\D:\Dev\repos\bumi-mcp", "python", "-m", "bumi_mcp"],
      "env": { "PYTHONPATH": "\D:\Dev\repos\bumi-mcp/src" }
    }
  }
}
\\\

## Tools

- **bumi_tool**: bumi_tool

## Requirements

- Python 3.12+
- uv
