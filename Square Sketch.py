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

        # Create an object collection for the points.
        points = adsk.core.ObjectCollection.create()

        # Define the points the spline with fit through.
        points.add(adsk.core.Point3D.create(1, 0, 0))
        points.add(adsk.core.Point3D.create(0, -1, 0))
        points.add(adsk.core.Point3D.create(-1, 0, 0))
        points.add(adsk.core.Point3D.create(0, 1, 0))

        # Connect the Lines.
        for i in range(points.count -1):
                start_point = points.item(0)
                pt1 = points.item(i)
                pt2 = points.item(i+1)
                sketch.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)

                if(i == points.count -2):
                    sketch.sketchCurves.sketchLines.addByTwoPoints(start_point, pt2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
