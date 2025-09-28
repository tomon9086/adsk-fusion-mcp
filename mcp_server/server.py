import xmlrpc.client

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

mcp = FastMCP(
    "FusionMCP",
    instructions="Support Free AI Generative Design with MCP",
)


class FusionRPCClient:
    def __init__(self, host="localhost", port=9875):
        self.host = host
        self.port = port
        self.server = xmlrpc.client.ServerProxy(
            f"http://{host}:{port}", allow_none=True
        )

    def ping(self) -> TextContent:
        result = self.server.ping()
        return TextContent(type="text", text="success" if result else "failed")

    def create_cylinder(
        self, x: float, y: float, z: float, radius: float, height: float
    ) -> TextContent:
        result = self.server.create_cylinder(x, y, z, radius, height)
        return TextContent(type="text", text="success" if result else "failed")


@mcp.tool()
def ping(ctx: Context) -> list[TextContent]:
    """Send a ping to Fusion RPC server.

    Args:
        host: Host of Fusion RPC server (default: localhost)
        port: Port of Fusion RPC server (default: 9875)

    Returns:
        Ping result message
    """
    client = FusionRPCClient()
    result = client.ping()
    return [result]


@mcp.tool()
def create_cylinder(
    ctx: Context,
    x: float,
    y: float,
    z: float,
    radius: float,
    height: float,
) -> list[TextContent]:
    """Create a cylinder in Fusion.

    Args:
        x: X coordinate of the cylinder center
        y: Y coordinate of the cylinder center
        z: Z coordinate of the cylinder center
        radius: Radius of the cylinder
        height: Height of the cylinder
    Returns:
        Result message
    """
    client = FusionRPCClient()
    result = client.create_cylinder(x, y, z, radius, height)
    return [result]


def main():
    mcp.run()
