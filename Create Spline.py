#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

        # Create an object collection for the points.
        points = adsk.core.ObjectCollection.create()

        # Define the points the spline with fit through.
        points.add(adsk.core.Point3D.create(0, 0, 0))
        points.add(adsk.core.Point3D.create(5, 1, 0))
        points.add(adsk.core.Point3D.create(6, 4, 3))
        points.add(adsk.core.Point3D.create(7, 6, 6))
        points.add(adsk.core.Point3D.create(2, 3, 0))
        points.add(adsk.core.Point3D.create(0, 1, 0))

        # Create the spline.
        for i in range(points.count -1):
            pt1 = points.item(i)
            pt2 = points.item(i+1)
            sketch.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
