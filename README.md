# Autodesk Fusion MCP

Support Free AI Generative Design with MCP

## Setup

### Setup MCP Server

Claude Desktop: `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fusion": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/tomon9086/adsk-fusion-mcp",
        "fusion-mcp"
      ]
    }
  }
}
```
