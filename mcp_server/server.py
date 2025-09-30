import xmlrpc.client

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

from .types import RpcResponse

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
        result = RpcResponse.of(self.server.ping())
        return TextContent(type="text", text=result.message)

    def extrude_profile(self, sketch_name: str, distance: float) -> TextContent:
        result = RpcResponse.of(self.server.extrude_profile(sketch_name, distance))
        return TextContent(type="text", text=result.message)

    def create_sketch_circle(
        self, plane: str, coords: list[float], radius: float
    ) -> TextContent:
        result = RpcResponse.of(self.server.create_sketch_circle(plane, coords, radius))
        return TextContent(type="text", text=result.message)

    def create_sketch_rectangle(
        self, plane: str, point_one: list[float], point_two: list[float]
    ) -> TextContent:
        result = RpcResponse.of(
            self.server.create_sketch_rectangle(plane, point_one, point_two)
        )
        return TextContent(type="text", text=result.message)


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
def extrude_profile(
    ctx: Context, sketch_name: str, distance: float
) -> list[TextContent]:
    """Extrude a profile in Fusion.

    Args:
        sketch_name: Name of the sketch to extrude
        distance: Distance to extrude

    Returns:
        Result message
    """
    client = FusionRPCClient()
    result = client.extrude_profile(sketch_name, distance)
    return [result]


@mcp.tool()
def create_sketch_circle(
    ctx: Context, plane: str, coords: list[float], radius: float
) -> list[TextContent]:
    """Create a sketch circle in Fusion.

    Args:
        plane: Construction plane to use ('xy', 'yz', 'xz')
        coords: Center point of the circle
        radius: Radius of the circle

    Returns:
        Result message
    """
    client = FusionRPCClient()
    result = client.create_sketch_circle(plane, coords, radius)
    return [result]


@mcp.tool()
def create_sketch_rectangle(
    ctx: Context, plane: str, point_one: list[float], point_two: list[float]
) -> list[TextContent]:
    """Create a sketch rectangle in Fusion.

    Args:
        plane: Construction plane to use ('xy', 'yz', 'xz')
        point_one: First corner point of the rectangle; (x, y)
        point_two: Opposite corner point of the rectangle; (x, y)

    Returns:
        Result message
    """
    client = FusionRPCClient()
    result = client.create_sketch_rectangle(plane, point_one, point_two)
    return [result]


def main():
    mcp.run()
