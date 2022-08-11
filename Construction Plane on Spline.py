#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        number_of_points = 4 
         
        points_float = [[0]*3 for i in range (number_of_points)]
        points_float[0]= [0,0,0]
        points_float[1]= [0,0,10]
        points_float[2]= [3,0,14]
        points_float[3]= [10,0,15]

        #Example values include 
        # 0,0,0; 
        # 0, 0, 10; 
        # 3, 0, 14; 
        # 10, 0, 15;

        design = app.activeProduct
        rootComp = design.rootComponent
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = []
        spline = []

        points.append(adsk.core.ObjectCollection.create())
        for i in range (number_of_points):
            points[0].add(adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2]))
        spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))

        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #We are going to get the first item in the sketch which should be our spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath = sketch1.sketchCurves.sketchFittedSplines.item(0)

        for i in range (100):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
            distance = adsk.core.ValueInput.createByReal(i/100) 
            planeInput.setByDistanceOnPath(crvPath, distance)
            plane = planes.add(planeInput)
            #Add new Sketch
            rootComp.sketches.add(plane)



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
