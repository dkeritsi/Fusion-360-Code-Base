#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def circle_create (sketch, x, y, z, radius):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), radius)
        prof = sketch.profiles.item(0)
        return prof 

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        number_of_points = 4 #Number of points for Spline
        radius = 1 #Radius for Pipe
        #ui.messageBox("Please enter in " + str(number_of_points) + " points for Pipe Spline.")
        points_float = [[0]*3 for i in range (number_of_points)]
        theta = 20

        #Example values include 
        # 0,0,0; 
        # 0, 0, 10; 
        # 3, 0, 14; 
        # 10, 0, 15;

        points_float[0]= [0,0,0]
        points_float[1]= [0,0,10]
        points_float[2]= [-10,0,10]
        points_float[3]= [-10,0,15]

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
        circle_prof = circle_create(sketch, points_float[0][0] ,points_float[0][1], points_float[0][2], radius) #We want to sweep the first sketch which should be the circle

        ui.messageBox("Circle Sketched Complete.")

        # Create a sweep input
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(circle_prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Create the sweep.
        sweeps.add(sweepInput)
        ui.messageBox("Sweeping Complete based on Circle and Spline Path.")

        #Set up Construction Planes along Spline 
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #Create a Path based on the Spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath_spline = sketch1.sketchCurves.sketchFittedSplines.item(0)

        #Note: 400 construction planes were created, 23 buildable bodies were created. By contrast, when 100 were create, only 16 builable bodies were created.
        number_of_planes = 100
        layer_bound_count = 0
        for i in range (number_of_planes):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
            distance = adsk.core.ValueInput.createByReal(i/number_of_planes) 
            planeInput.setByDistanceOnPath(crvPath_spline, distance)
            plane_i = planes.add(planeInput)

            #Extract features from the construction plane
            plane_object = plane_i.geometry 
            u_vector = plane_object.uDirection
            v_vector = plane_object.vDirection
            cross_product_u_v = u_vector.crossProduct(v_vector)

            #We want the build direction to be equal to the first construction plane 
            if i == 0:
                build_path_normal = cross_product_u_v

            angle_between = cross_product_u_v.angleTo(build_path_normal)

            #ui.messageBox("The angel between is: " + str(math.degrees(angle_between)))

            if math.degrees(angle_between) > theta:
                #Place Sketch at Same Location of Construction Plane
                sketch = sketches.add(plane_i) #Sketch Plane can be passed an object type of Construction Plane
                circles = sketch.sketchCurves.sketchCircles
                circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius) #Set <0,0,0> since this coextensive with instant Construction Plane

                #Extrude
                #extrudes = rootComp.features.extrudeFeatures
                #dist = adsk.core.ValueInput.createByReal(.1) 
                #profile_of_circle = sketch.profiles.item(0)
                #extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
                #extrudeInput.setDistanceExtent(False, dist)
                #extrudes.add(extrudeInput)

                #distance = adsk.core.ValueInput.createByReal(1000)
                #extrudes.addSimple(profile_of_circle, distance, adsk.fusion.FeatureOperations.IntersectFeatureOperation)

                #After Extruding, now we want to set the build direction EQUAL to the instant construction plane (similar to if i=0)
                build_path_normal = cross_product_u_v
                layer_bound_count = layer_bound_count + 1
                    
        ui.messageBox("Slicing Body Complete")
        ui.messageBox("The number of Layer Boundaries is: " + str(layer_bound_count) + " which are represented as sketches.")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


