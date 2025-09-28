import os
import sys
import traceback

import adsk.core

addin_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(addin_path, "lib")
if lib_path not in sys.path:
    sys.path.append(lib_path)

from lib.rpc.server import FusionRPCServer

app = None
ui = None
rpc_server = None


def run(context):
    global app
    global ui
    global rpc_server

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

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
