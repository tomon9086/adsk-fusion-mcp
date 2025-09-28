import os
import sys
import traceback
from datetime import datetime

import adsk.core

addin_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, addin_path)

# Force module reload by removing from sys.modules
modules_to_reload = [key for key in sys.modules.keys() if key.startswith("lib.")]
for module in modules_to_reload:
    if module in sys.modules:
        del sys.modules[module]

from lib.rpc.server import FusionRPCServer

app = None
ui = None
rpc_server = None


def flush_console(app: adsk.core.Application):
    """Flush Text Commands Window (for debugging)"""
    app.log("\n\n\n\n=== {} ===".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


def run(context):
    global app
    global ui
    global rpc_server

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        flush_console(app)

        rpc_server = FusionRPCServer()
        rpc_server.start()

        ui.messageBox("Started Fusion MCP\nRPC Server is running on port 9875")

    except:
        if ui:
            ui.messageBox("ERROR:\n{}".format(traceback.format_exc()))


def stop(context):
    global ui
    global rpc_server

    try:
        if rpc_server:
            rpc_server.stop()
            rpc_server = None
            ui.messageBox("Stopped Fusion MCP")
        else:
            ui.messageBox("RPC Server is already stopped")

    except:
        if ui:
            ui.messageBox("ERROR:\n{}".format(traceback.format_exc()))
