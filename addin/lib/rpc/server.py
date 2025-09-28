import threading
from xmlrpc.server import SimpleXMLRPCServer


class FusionRPCMethods:
    def ping(self):
        """ping
        Check if the server is alive
        """
        return True


class FusionRPCServer:
    def __init__(self, host="localhost", port=9875):
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None
        self.is_running = False

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
