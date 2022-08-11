#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        unitsMgr = design.unitsManager

        ui.messageBox('Please enter in four points for Pipe Spline.')
        input = ''
        retVals = ui.inputBox("Enter the first number for the Pipe Spline.", 'Point', input)

        if retVals[0]:
                (input, isCancelled) = retVals
            
            # Exit the program if the dialog was cancelled.
        if isCancelled:
                return

        ui.messageBox("This is the value entered:" + input)

        

         
        # Get the root component of the active design.
        rootComp = design.rootComponent
         
        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
         
        points = []
        spline = []
        # Create an object collection for the points.
        points.append(adsk.core.ObjectCollection.create())
        # Define the points the spline with fit through.
        points[0].add(adsk.core.Point3D.create(0, 0, 0))
        points[0].add(adsk.core.Point3D.create(5, 1, 0))
        points[0].add(adsk.core.Point3D.create(6, 4, 3))
        # Create the spline.
        spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))
         
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        # Create an object collection for the points.
        points.append(adsk.core.ObjectCollection.create())
        points[1].add(adsk.core.Point3D.create(7, 6, 6))
        points[1].add(adsk.core.Point3D.create(2, 3, 0))
        points[1].add(adsk.core.Point3D.create(0, 1, 0))
        # Create the spline.
        spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[1]))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
