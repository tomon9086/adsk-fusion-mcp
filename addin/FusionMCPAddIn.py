import traceback

import adsk.core


def run(context):
    global app
    global ui

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        ui.messageBox("Hello, World!")

    except:
        if ui:
            ui.messageBox("ERROR:\n{}".format(traceback.format_exc()))


def stop(context):
    global ui

    try:
        ui.messageBox("Stopped!")

    except:
        if ui:
            ui.messageBox("ERROR:\n{}".format(traceback.format_exc()))
