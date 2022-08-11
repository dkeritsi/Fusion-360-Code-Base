#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)

        #Constrain Circle Size
        #sketch.sketchDimensions.addDiameterDimension(circle1, adsk.core.Point3D.create(3, 3, 0))

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        #Extrude Distance
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(5))

        #Create the Extrusion
        ext = extrudes.add(extInput)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
