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

        # Get the root component of the active design.
        rootComp = design.rootComponent
         
        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        ui.messageBox('Please enter in four points for Pipe Spline.')
        points = []
        #points.append(adsk.core.ObjectCollection.create())
        i = 0
        for i in range (4):
            input_x = ''
            input_y = ''
            input_z = ''
            #retVals = ui.inputBox("Enter the first number for the Pipe Spline.", 'Point', input)
            retVals_x = ui.inputBox("Enter x point " + str(i) + " for the Pipe Spline.", 'Point', input_x)
            retVals_y = ui.inputBox("Enter y point " + str(i) + " for the Pipe Spline.", 'Point', input_y)
            retVals_z = ui.inputBox("Enter z point " + str(i) + " for the Pipe Spline.", 'Point', input_z)
            #points[i].add(adsk.core.Point3D.create(input_x, input_y, input_z))
            if retVals_x[0]:
                (input_x, isCancelled) = retVals_x
            if retVals_y[0]:
                (input_y, isCancelled) = retVals_y
            if retVals_z[0]:
                (input_z, isCancelled) = retVals_z
                
                # Exit the program if the dialog was cancelled.
            if isCancelled:
                    return

            ui.messageBox("This is the x value entered:" + input_x)
            ui.messageBox("This is the y value entered:" + input_y)
            ui.messageBox("This is the z value entered:" + input_z)

            

         
        #spline = []
        #spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))
         
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
