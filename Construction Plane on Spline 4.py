#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import array as arrA

def circle_create_extrude (sketch, root, x, y, z):
        #####Create Body #####
        #Sketch Circle
        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), 2)

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude
        extrudes = root.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        #Extrude Distance
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10))

        #Create the Extrusion
        extrudes.add(extInput)

        return extrudes

def circle_create (sketch, root, x, y, z):
        #####Create Body #####
        #Sketch Circle
        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), 2)

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude

        #return 0 
        return prof 

def calculateTightBoundingBox(body, tolerance = 0):
    try:
        # If the tolerance is zero, use the best display mesh available.
        if tolerance <= 0:
            # Get the best display mesh available.
            triMesh = body.meshManager.displayMeshes.bestMesh
        else:
            # Calculate a new mesh based on the input tolerance.
            meshMgr = adsk.fusion.MeshManager.cast(body.meshManager)
            meshCalc = meshMgr.createMeshCalculator()
            meshCalc.surfaceTolerance = tolerance
            triMesh = meshCalc.calculate()
   
        # Calculate the range of the mesh.
        smallPnt = adsk.core.Point3D.cast(triMesh.nodeCoordinates[0])
        largePnt = adsk.core.Point3D.cast(triMesh.nodeCoordinates[0])
        vertex = adsk.core.Point3D.cast(None)
        for vertex in triMesh.nodeCoordinates:
            if vertex.x < smallPnt.x:
                smallPnt.x = vertex.x
               
            if vertex.y < smallPnt.y:
                smallPnt.y = vertex.y
               
            if vertex.z < smallPnt.z:
                smallPnt.z = vertex.z
           
            if vertex.x > largePnt.x:
                largePnt.x = vertex.x

            if vertex.y > largePnt.y:
                largePnt.y = vertex.y
               
            if vertex.z > largePnt.z:
                largePnt.z = vertex.z
               
        # Create and return a BoundingBox3D as the result.
        return(adsk.core.BoundingBox3D.create(smallPnt, largePnt))
    except:
        # An error occurred so return None.
        return(None)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        #***Enter Points for Spline***
        number_of_points = 4 
        ui.messageBox("Please enter in " + str(number_of_points) + " points for Pipe Spline.")
        inputs_string = [['']*3 for i in range (number_of_points)]
        points_float = [[0]*3 for i in range (number_of_points)]
        i = 0
        preset = 1  #WE NEED TO REMOVE THIS BECAUSE THIS IS FOR TESTING

        #Example values include 
        # 0,0,0; 
        # 0, 0, 10; 
        # 3, 0, 14; 
        # 10, 0, 15;
        if (preset == 0):
            for i in range (number_of_points):
                input_x = ''
                input_y = ''
                input_z = ''
                retVals_x = ui.inputBox("Enter x point " + str(i) + " for the Pipe Spline.", 'Point', input_x)
                retVals_y = ui.inputBox("Enter y point " + str(i) + " for the Pipe Spline.", 'Point', input_y)
                retVals_z = ui.inputBox("Enter z point " + str(i) + " for the Pipe Spline.", 'Point', input_z)
                if retVals_x[0]:
                    (input_x, isCancelled) = retVals_x
                if retVals_y[0]:
                    (input_y, isCancelled) = retVals_y
                if retVals_z[0]:
                    (input_z, isCancelled) = retVals_z
                
                    # Exit the program if the dialog was cancelled.
                if isCancelled:
                        return

                inputs_string[i] = [input_x, input_y, input_z] 
                points_float[i] = [float(input_x), float(input_y), float(input_z)] 

            #ui.messageBox("For point " + str(i) + ", this is the x value entered:" + inputs_string[i][0])
            #ui.messageBox("For point " + str(i) + ", this is the y value entered:" + inputs_string[i][1])
            #ui.messageBox("For point " + str(i) + ", this is the z value entered:" + inputs_string[i][2])

        if(preset == 1):
            points_float[0]= [0,0,0]
            points_float[1]= [0,0,10]
            points_float[2]= [3,0,14]
            points_float[3]= [10,0,15]

        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = []
        spline = []

        points.append(adsk.core.ObjectCollection.create())
        for i in range (number_of_points):
            points[0].add(adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2]))
        spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))


         #We are going to get the first item in the sketch which should be our spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath = sketch1.sketchCurves.sketchFittedSplines.item(0)#THIS IS HARD CODED!!!!

        ui.messageBox("Construction of Splines Complete.")

        #Create Construction Planes along Spline ***Lets take out Construction Planes out now***
        #planes = rootComp.constructionPlanes
        #planeInput = planes.createInput()
        #for i in range (100):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
        #    distance = adsk.core.ValueInput.createByReal(i/100) 
        #    planeInput.setByDistanceOnPath(crvPath, distance)
        #    plane = planes.add(planeInput)
            #Add new Sketch
        #    rootComp.sketches.add(plane)


        #ui.messageBox("Construction Planes running along Spline Complete.")

        #New Sketch on xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #Create Circle and Extrude
        #extrudes = circle_create_extrude(sketch, rootComp)        
        #extrudes = rootComp.features.extrudeFeatures

        circle_prof = circle_create(sketch, rootComp, 0 ,0, 0) #We want to sweep the first sketch which should be the circle

        ui.messageBox("Circle Sketched Complete.")

    # Create a sweep input
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(circle_prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        #sweepInput.guideRail = guide
        #sweepInput.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileScaleOption
        
        # Create the sweep.
        sweep = sweeps.add(sweepInput)

        ui.messageBox("Sweeping Complete based on Circle and Spline Path.")

    


    #Now we want to Extrude along the Spline which should be sketch item(0) 
    #circles = sketch.sketchCurves.sketchCircles
    #circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(points_float[0][0],points_float[0][1],points_float[0][2]), 2)
        #prof = sketch.profiles.item(0)
        #extrudes = rootComp.features.extrudeFeatures
        #extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)


        #Extrude
        #extrudes = rootComp.features.extrudeFeatures
        #extInput



        #We want to have the Bounding Box and Select the Body AFTER Sweeping
 




    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
