#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        prof = sketch.profiles.item(0)
        prof1 = sketch.profiles.item(1)

        ui.messageBox("This is the first profile:" + prof)
        ui.messageBox("This is the first profile:" + prof1)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
