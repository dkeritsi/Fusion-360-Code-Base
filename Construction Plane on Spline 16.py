#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def circle_create (sketch, x, y, z, radius):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), radius)
        prof = sketch.profiles.item(0)
        return prof 

def construction_of_splines(points, points_float, spline, sketch, number_of_points):
    ui  = adsk.core.Application.get().userInterface
    points.append(adsk.core.ObjectCollection.create())
    for i in range (number_of_points):
        points[0].add(adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2]))
    spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))
    ui.messageBox("Construction of Splines Complete.")

def create_body(points_float, radius, spline):
        ui  = adsk.core.Application.get().userInterface
        rootComp = adsk.core.Application.get().activeProduct.rootComponent

        #New Sketch on xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        circle_prof_outter = circle_create(sketch, points_float[0][0] ,points_float[0][1], points_float[0][2], radius*2) #We want to sweep the first sketch which should be the circle
        ui.messageBox("Circle Sketched Complete.")

        # Create a sweep input
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput_outter = sweeps.createInput(circle_prof_outter, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Create the sweep.
        sweeps.add(sweepInput_outter)
        ui.messageBox("Sweeping Complete based on Circle and Spline Path.")

        # Create the sweep via intersect.
        circle_prof_inner = circle_create(sketch, points_float[0][0] ,points_float[0][1], points_float[0][2], radius) #We want to sweep the first sketch which should be the circle
        sweepInput_inner = sweeps.createInput(circle_prof_inner, path, adsk.fusion.FeatureOperations.IntersectFeatureOperation)
        sweeps.add(sweepInput_inner)

        #Create Construction Planes along Spline 
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #Create a Path based on the Spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath_spline = sketch1.sketchCurves.sketchFittedSplines.item(0)

        return planeInput, crvPath_spline, planes, sketches

def run_along_spline(number_of_construction_planes, planeInput, crvPath_spline, planes, radius, sketches):
        ui  = adsk.core.Application.get().userInterface
        rootComp = adsk.core.Application.get().activeProduct.rootComponent

        for i in range (number_of_construction_planes):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
            distance = adsk.core.ValueInput.createByReal(i/number_of_construction_planes) 
            planeInput.setByDistanceOnPath(crvPath_spline, distance)
            plane_i = planes.add(planeInput)

            #Get the center point of the Construction Plane
            inter_pt_i = plane_i.geometry.intersectWithCurve(crvPath_spline.worldGeometry)
            x = inter_pt_i.item(0).x
            y = inter_pt_i.item(0).y
            z = inter_pt_i.item(0).z

            #Extract features from the construction plane
            plane_object = plane_i.geometry 
            u_vector = plane_object.uDirection
            v_vector = plane_object.vDirection
            cross_product_u_v = u_vector.crossProduct(v_vector)

            #We want the build direction to be equal to the first construction plane 
            if i == 0:
                normal = cross_product_u_v

            dot_product = cross_product_u_v.dotProduct(normal)
            angle_between = cross_product_u_v.angleTo(normal)

            if math.degrees(angle_between) > 20:
                #Place Sketch at Same Location of Construction Plane
                sketch = sketches.add(plane_i) #Sketch Plane can be passed an object type of Construction Plane
                circles = sketch.sketchCurves.sketchCircles
                circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius*3) #Set <0,0,0> since this coextensive with instant Construction Plane

                #Extrude
                extrudes = rootComp.features.extrudeFeatures
                dist = adsk.core.ValueInput.createByReal(.1) 
                prof = sketch.profiles.item(0)
                extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extrudeInput.setDistanceExtent(False, dist)
                extrudes.add(extrudeInput)

                #After Extruding, now we want to set the build direction EQUAL to the instant construction plane (similar to if i=0)
                normal = cross_product_u_v
                    
        ui.messageBox("Construction Planes running along Spline Complete.")

def points_of_spline(number_of_points):
    app = adsk.core.Application.get()
    rootComp = app.activeProduct.rootComponent

    points_float_set = [[0]*3 for i in range (number_of_points)]
    points = []
    spline = []
    sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    return points_float_set, sketch, points, spline, number_of_points

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        radius = 2 #Radius for Pipe
        number_of_construction_planes = 100 #Number of Construction Planes per Path/Spline

        #First Path 
        points_float_set_1, sketch, points, spline, number_of_points_1 = points_of_spline(number_of_points = 4)

        points_float_set_1[0]= [0,0,0]
        points_float_set_1[1]= [0,0,10]
        points_float_set_1[2]= [-3,0,14]
        points_float_set_1[3]= [-10,0,15]


        #Second Path 
        points_float_set_2, sketch2, points2, spline2, number_of_points_2 = points_of_spline(number_of_points= 4)

        points_float_set_2[0]= [-10,0,15]
        points_float_set_2[1]= [-15,0,15]
        points_float_set_2[2]= [-20,0,15]
        points_float_set_2[3]= [-30,0,15]


        #Third Path 
        points_float_set_3, sketch3, points3, spline3, number_of_points_3 = points_of_spline(number_of_points = 4)

        points_float_set_3[0]= [-30,0,15]
        points_float_set_3[1]= [-30,0,20]
        points_float_set_3[2]= [-30,0,25]
        points_float_set_3[3]= [-30,0,30]


        #Construct Spline/Line
        construction_of_splines(points, points_float_set_1, spline, sketch, number_of_points_1) 
        construction_of_splines(points2, points_float_set_2, spline2, sketch2, number_of_points_2) 
        construction_of_splines(points3, points_float_set_3, spline3, sketch3, number_of_points_3) 

        #Create Body to be Cut
        planeInput, crvPath_spline, planes, sketches = create_body(points_float_set_1, radius, spline)

        #Place Construction PLanes along Spline and Cut
        run_along_spline(number_of_construction_planes, planeInput, crvPath_spline, planes, radius, sketches)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



