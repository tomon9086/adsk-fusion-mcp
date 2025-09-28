from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "FusionMCP",
    instructions="Support Free AI Generative Design with MCP",
)


def main():
    mcp.run()
