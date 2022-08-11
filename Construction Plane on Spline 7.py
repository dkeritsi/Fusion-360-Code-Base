#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def circle_create (sketch, root, x, y, z):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), 2)
        prof = sketch.profiles.item(0)
        return prof 

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        number_of_points = 4 
        ui.messageBox("Please enter in " + str(number_of_points) + " points for Pipe Spline.")
        inputs_string = [['']*3 for i in range (number_of_points)]
        points_float = [[0]*3 for i in range (number_of_points)]

        preset = 1  #WE NEED TO REMOVE THIS BECAUSE THIS IS FOR TESTING

        #Example values include 
        # 0,0,0; 
        # 0, 0, 10; 
        # 3, 0, 14; 
        # 10, 0, 15;
        if (preset == 0):
            #***Enter Points for Spline***
            i = 0
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

        ui.messageBox("Construction of Splines Complete.")
      
        #New Sketch on xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        circle_prof = circle_create(sketch, rootComp, points_float[0][0] ,points_float[0][1], points_float[0][2]) #We want to sweep the first sketch which should be the circle

        ui.messageBox("Circle Sketched Complete.")

        # Create a sweep input
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(circle_prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Create the sweep.
        sweeps.add(sweepInput)
        ui.messageBox("Sweeping Complete based on Circle and Spline Path.")

        #Create Construction Planes along Spline 
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #Create a Path based on the Spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath_spline = sketch1.sketchCurves.sketchFittedSplines.item(0)

        # Create the sweep.
        normal_vectors = [[0]*10 for i in range (10)] #We want an array of normal vectors
        normal_vectors[0] = 20 #Just set the first normal vectors in array

        for i in range (100):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
            distance = adsk.core.ValueInput.createByReal(i/100) 
            planeInput.setByDistanceOnPath(crvPath_spline, distance)
            plane_i = planes.add(planeInput)
            #Add new Sketch
            #new_plane_i = rootComp.sketches.add(plane_i)
            if i == 1:
                object_type = plane_i.objectType
                ui.messageBox("plane_i is type:" + object_type) #This should be type Construction Plane
                inter_pt_i = plane_i.geometry.intersectWithCurve(crvPath_spline.worldGeometry)
                x = inter_pt_i.item(0).x
                y = inter_pt_i.item(0).y
                z = inter_pt_i.item(0).z

                ui.messageBox("This is the location of the construction plane" +"X = "+str(x)+ "  Y = " + str(y) + "  Z = "+str(z))
                #object_type = new_plane_i.objectType
                #ui.messageBox("new_plane_i is type:" + object_type) #This should be type Sketch
                #vector = adsk.core.Vector3D.create(0,0,1) 
                #adsk.core.Vector3D.add(vector)
                #This should be Sket type
            #vector = new_plane_i.vDirection
            #adsk.core.Vector3D.add(vector)


        ui.messageBox("Construction Planes running along Spline Complete.")
        ui.messageBox("Slicing Body Complete")

        number_of_planes = planes.count
        ui.messageBox("The number of planes create is:" + str(number_of_planes))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
