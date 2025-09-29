import os
import sys
import threading
from xmlrpc.server import SimpleXMLRPCServer

import adsk.core

from .types import RpcResponse

lib_rpc_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(lib_rpc_path, "../../..")
lib_path = os.path.join(root_path, "addin/lib")
sys.path.insert(0, lib_path)

from lib.commands.extrude_profile import extrude_profile
from lib.commands.sketch import create_sketch
from lib.commands.sketch_circle import create_sketch_circle


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
            design = app.activeProduct
            root_component = design.rootComponent

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
            design = app.activeProduct
            root_component = design.rootComponent

            construction_plane = None
            if plane == "xy":
                construction_plane = root_component.xYConstructionPlane
            elif plane == "yz":
                construction_plane = root_component.yZConstructionPlane
            elif plane == "xz":
                construction_plane = root_component.xZConstructionPlane

            if construction_plane is None:
                raise ValueError(f"Invalid plane '{plane}'. Use 'xy', 'yz', or 'xz'.")

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
                    "name: {}".format(circle.name),
                ],
            ).to_dict()

        except Exception as e:
            app.log(f"Error in create_sketch_circle RPC method: {str(e)}")
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
