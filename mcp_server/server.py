import xmlrpc.client

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

mcp = FastMCP(
    "FusionMCP",
    instructions="Support Free AI Generative Design with MCP",
)


@mcp.tool()
def ping(ctx: Context, host: str = "localhost", port: int = 9875) -> list[TextContent]:
    """Send a ping to Fusion RPC server.

    Args:
        host: Host of Fusion RPC server (default: localhost)
        port: Port of Fusion RPC server (default: 9875)

    Returns:
        Ping result message
    """
    try:
        # Create RPC client
        server = xmlrpc.client.ServerProxy(f"http://{host}:{port}", allow_none=True)

        # Call ping endpoint
        result = server.ping()

        if result:
            return [
                TextContent(
                    type="text",
                    text=f"✅ Successfully connected to Fusion RPC server ({host}:{port}).",
                )
            ]
        else:
            return [
                TextContent(
                    type="text",
                    text=f"❌ Invalid response from Fusion RPC server ({host}:{port}).",
                )
            ]

    except ConnectionError:
        return [
            TextContent(
                type="text",
                text=f"❌ Failed to connect to Fusion RPC server ({host}:{port}). Please check if the server is running.",
            )
        ]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ An error occurred: {str(e)}")]


def main():
    mcp.run()
