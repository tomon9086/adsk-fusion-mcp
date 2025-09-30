import os
import sys
import threading
from xmlrpc.server import SimpleXMLRPCServer

import adsk.core
import adsk.fusion

from .types import RpcResponse

lib_rpc_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(lib_rpc_path, "../../..")
lib_path = os.path.join(root_path, "addin/lib")
sys.path.insert(0, lib_path)

from lib.commands.extrude_profile import extrude_profile
from lib.commands.sketch_circle import create_sketch_circle
from lib.commands.sketch_rectangle import create_sketch_rectangle


def get_root_component(app: adsk.core.Application) -> adsk.fusion.Component:
    design = app.activeProduct
    if not isinstance(design, adsk.fusion.Design):
        raise RuntimeError("No active Fusion design")

    return design.rootComponent


def get_plane_by_name(
    component: adsk.fusion.Component, name: str
) -> adsk.fusion.ConstructionPlane:
    name = name.lower()
    if name == "xy":
        return component.xYConstructionPlane
    elif name == "yz":
        return component.yZConstructionPlane
    elif name == "xz":
        return component.xZConstructionPlane
    else:
        raise ValueError(f"Invalid plane name: {name}")


class FusionRPCMethods:
    def ping(self) -> dict:
        """ping
        Check if the server is alive
        """

        return RpcResponse(success=True, message="Pong").to_dict()

    def extrude_profile(self, sketch_name: str, distance: float) -> dict:
        """Extrude a profile"""
        try:
            app = adsk.core.Application.get()
            root_component = get_root_component(app)

            # Find the sketch by name
            sketches = root_component.sketches
            target_sketch = next(
                (sketch for sketch in sketches if sketch.name == sketch_name), None
            )

            if target_sketch is None:
                raise ValueError(f"Sketch '{sketch_name}' not found")

            # Extrude the profile
            extrude = extrude_profile(
                component=root_component, sketch=target_sketch, distance=distance
            )
            if extrude is None:
                raise RuntimeError("Failed to extrude the profile")

            return RpcResponse(
                success=True, message="Profile extruded successfully"
            ).to_dict()

        except Exception as e:
            app.log(f"Error in extrude_profile RPC method: {str(e)}")
            return RpcResponse(success=False, message=str(e)).to_dict()

    def create_sketch_circle(
        self, plane: str, coords: list[float], radius: float
    ) -> dict:
        """Create a new sketch circle"""
        try:
            app = adsk.core.Application.get()
            root_component = get_root_component(app)
            construction_plane = get_plane_by_name(root_component, plane)

            # Create a circle in the sketch
            circle = create_sketch_circle(
                component=root_component,
                plane=construction_plane,
                coords=adsk.core.Point3D.create(*coords),
                radius=radius,
            )

            if circle is None:
                raise RuntimeError("Failed to create sketch circle")

            return RpcResponse(
                success=True,
                message=[
                    "Sketch circle created successfully",
                    "name: {}".format(circle.parentSketch.name),
                ],
            ).to_dict()

        except Exception as e:
            app.log(f"Error in create_sketch_circle RPC method: {str(e)}")
            return RpcResponse(success=False, message=str(e)).to_dict()

    def create_sketch_rectangle(
        self, plane: str, point_one: list[float], point_two: list[float]
    ) -> dict:
        """Create a new sketch rectangle"""
        try:
            app = adsk.core.Application.get()
            root_component = get_root_component(app)
            construction_plane = get_plane_by_name(root_component, plane)

            # Create a rectangle in the sketch
            rectangle = create_sketch_rectangle(
                component=root_component,
                plane=construction_plane,
                point_one=adsk.core.Point3D.create(*point_one),
                point_two=adsk.core.Point3D.create(*point_two),
            )

            return RpcResponse(
                success=True,
                message=[
                    "Sketch rectangle created successfully",
                    "name: {}".format(rectangle.name),
                ],
            ).to_dict()

        except Exception as e:
            app.log(f"Error in create_sketch_rectangle RPC method: {str(e)}")
            return RpcResponse(success=False, message=str(e)).to_dict()


class FusionRPCServer:
    def __init__(self, host="localhost", port=9875):
        try:
            self.host = host
            self.port = port
            self.server = None
            self.server_thread = None
            self.is_running = False

        except Exception as e:
            print(f"Error in FusionRPCServer.__init__: {str(e)}")
            raise

    def start(self):
        """Start the server"""
        if self.is_running:
            return

        try:
            # Create RPC server
            self.server = SimpleXMLRPCServer((self.host, self.port), allow_none=True)

            # Register methods
            rpc_methods = FusionRPCMethods()
            self.server.register_function(rpc_methods.ping, "ping")

            self.server.register_function(
                rpc_methods.extrude_profile, "extrude_profile"
            )
            self.server.register_function(
                rpc_methods.create_sketch_circle, "create_sketch_circle"
            )
            self.server.register_function(
                rpc_methods.create_sketch_rectangle, "create_sketch_rectangle"
            )

            # Start the server in a separate thread
            self.server_thread = threading.Thread(target=self._serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.is_running = True

        except Exception as e:
            raise Exception(f"Failed to start RPC server: {str(e)}")

    def stop(self):
        """Stop the server"""
        if not self.is_running:
            return

        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()

            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=1)

            self.is_running = False

        except Exception as e:
            print(f"Error occurred while stopping RPC server: {str(e)}")

    def _serve_forever(self):
        """Server main loop"""
        try:
            self.server.serve_forever()
        except Exception as e:
            print(f"Error occurred while running RPC server: {str(e)}")
            self.is_running = False
