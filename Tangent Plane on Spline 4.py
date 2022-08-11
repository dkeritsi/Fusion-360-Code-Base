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
        number_of_points = 4
         
        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        ui.messageBox("Please enter in " + str(number_of_points) + " points for Pipe Spline.")
        inputs_string = [['']*3 for i in range (number_of_points)]
        points = [[0]*3 for i in range (number_of_points)]
        points.append(adsk.core.ObjectCollection.create())

        i = 0
        for i in range (number_of_points):
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

            #inputs[i] = [float(input_x), float(input_y), float(input_z)] 
            inputs_string[i] = [input_x, input_y, input_z] 
            points[i] = [float(input_x), float(input_y), float(input_z)] 
            #points[i].add(adsk.core.Point3D.create(float(input_x), float(input_y), float(input_z)))

            ui.messageBox("For point " + str(i) + ", this is the x value entered:" + inputs_string[i][0])
            ui.messageBox("For point " + str(i) + ", this is the y value entered:" + inputs_string[i][1])
            ui.messageBox("For point " + str(i) + ", this is the z value entered:" + inputs_string[i][2])

        

            

         
        #spline = []
        #spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))
         
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
