#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

#Creates a Circle Sketch at x, y, z with a radius
def circle_create_sketch(sketch, x, y, z, radius):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), radius)
        prof = sketch.profiles.item(0)
        return prof 

#Takes an array of points and creates a spline
def construction_of_splines(points, points_float, spline, number_of_points, sketch):
    ui  = adsk.core.Application.get().userInterface
    points.append(adsk.core.ObjectCollection.create())
    for i in range (number_of_points):
        points[0].add(adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2]))
    spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))
    ui.messageBox("Construction of Splines Complete.")

#Creates a Circle Profile based on a Construction Plane. The Construction Plane is in free space and not necessarily at 0, 0, 0.
def create_circle_prof(construction_plane_for_face, radius):
        ui  = adsk.core.Application.get().userInterface
        rootComp = adsk.core.Application.get().activeProduct.rootComponent
        sketches = rootComp.sketches
        sketch_for_face_outter = sketches.add(construction_plane_for_face)
        circle_prof_outter = circle_create_sketch(sketch_for_face_outter, 0, 0, 0, radius*2) #We want to sweep the first sketch which should be the circle
        ui.messageBox("Circle Sketched Complete.")
        return circle_prof_outter

#Takes Input of a Spline and a Prof (not necessarily a circle) and Sweeps to Create a New Body
def create_sweep_input_for_new_body(spline, prof):
        rootComp = adsk.core.Application.get().activeProduct.rootComponent
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        return sweepInput

#Takes Input of a Spline and a Prof (not necessarily a circle) and Sweeps to Cut a Body
def create_sweep_input_for_cut_body(spline, prof):
        rootComp = adsk.core.Application.get().activeProduct.rootComponent
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.CutFeatureOperation)
        return sweepInput

def create_pipe_body(inner_radius, outter_radius, spline, construction_plane_for_face):
        ui  = adsk.core.Application.get().userInterface
        rootComp = adsk.core.Application.get().activeProduct.rootComponent
        sketches = rootComp.sketches
        sweeps = rootComp.features.sweepFeatures

        #These are the inner and outter profiles for pipe 
        circle_prof_outter = create_circle_prof(construction_plane_for_face, outter_radius)
        circle_prof_inner = create_circle_prof(construction_plane_for_face, inner_radius)

        #Sketch for Outter 
        # (1a) Create a sweep input that comprises a profile and a spline
        sweepInput_outter = create_sweep_input_for_new_body(spline, circle_prof_outter) 
        
        # (1b) Create the sweep.
        sweeps.add(sweepInput_outter)
        ui.messageBox("Outter Sweeping Complete based on Circle and Spline Path.")

        #Sketch for Inner 
        # (1a) Create a sweep input that comprises a profile and a spline
        sweepInput_inner = create_sweep_input_for_cut_body(spline, circle_prof_inner) 
        
        # (1b) Create the sweep.
        sweeps.add(sweepInput_inner)
        ui.messageBox("Outter Sweeping Complete based on Circle and Spline Path.")

        #Create Construction Planes along Spline 
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #Create a Path based on the Spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath_spline = sketch1.sketchCurves.sketchFittedSplines.item(0)

        return planeInput, crvPath_spline, planes, sketches 

def run_along_spline_of_pipe(number_of_construction_planes, planeInput, crvPath_spline, planes, outter_radius, sketches):
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
                circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), outter_radius*3) #Set <0,0,0> since this coextensive with instant Construction Plane

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

def points_of_spline(number_of_points, sketch):
    points_float_set = [[0]*3 for i in range (number_of_points)]
    points = []
    spline = []
    return points_float_set, points, spline, number_of_points, sketch

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        outter_radius = 2 #Radius for Pipe
        inner_radius = 1 #Radius for Pipe
        number_of_construction_planes = 100 #Number of Construction Planes per Path/Spline

        #First Path 
        points_float_set_1, points1, spline1, number_of_points_1, sketch_1 = points_of_spline(number_of_points = 4, sketch = rootComp.sketches.add(rootComp.xYConstructionPlane))

        points_float_set_1[0]= [0,0,0]
        points_float_set_1[1]= [0,0,10]
        points_float_set_1[2]= [-3,0,14]
        points_float_set_1[3]= [-10,0,15]

        #Second Path 
        points_float_set_2, points2, spline2, number_of_points_2, sketch_2 = points_of_spline(number_of_points = 4, sketch = rootComp.sketches.add(rootComp.xYConstructionPlane))

        points_float_set_2[0]= [-10,0,15]
        points_float_set_2[1]= [-15,0,15]
        points_float_set_2[2]= [-20,0,15]
        points_float_set_2[3]= [-30,0,15]

        #Third Path 
        points_float_set_3, points3, spline3, number_of_points_3, sketch_3 = points_of_spline(number_of_points = 4, sketch = rootComp.sketches.add(rootComp.xYConstructionPlane))

        points_float_set_3[0]= [-30,0,15]
        points_float_set_3[1]= [-30,0,20]
        points_float_set_3[2]= [-30,0,25]
        points_float_set_3[3]= [-30,0,30]

        #Construct Spline/Line
        construction_of_splines(points1, points_float_set_1, spline1, number_of_points_1, sketch_1) 
        construction_of_splines(points2, points_float_set_2, spline2, number_of_points_2, sketch_2) 
        construction_of_splines(points3, points_float_set_3, spline3, number_of_points_3, sketch_3) 

        #Create Bodies ----
        #Create First Body 
        xyPlane = rootComp.xYConstructionPlane
        planeInput, crvPath_spline, planes, sketches = create_pipe_body(inner_radius, outter_radius, spline1, xyPlane)

        #Create Second Body
        #yzPLane = rootComp.yZConstructionPlane
        sketch = sketches.add(rootComp.xYConstructionPlane)
        sketchPoints = sketch.sketchPoints
        centerPoint = adsk.core.Point3D.create(-10, 0, 15)
        sketchCenterPoint = sketchPoints.add(centerPoint)
        positionTwo = adsk.core.Point3D.create(-10, 1, 0)
        sketchPointTwo = sketchPoints.add(positionTwo)
        positionThree = adsk.core.Point3D.create(-10, 0, 1)
        sketchPointThree = sketchPoints.add(positionThree)

        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()
        planeInput.setByThreePoints(sketchCenterPoint, sketchPointThree, sketchPointTwo)
        plane_2 = planes.add(planeInput)

        planeInput2, crvPath_spline2, planes2, sketches2 = create_pipe_body(inner_radius, outter_radius, spline2, plane_2)

        #Place Construction PLanes along Spline and Cut along First Body
        ui.messageBox("Start Slicing.")
        run_along_spline_of_pipe(number_of_construction_planes, planeInput, crvPath_spline, planes, outter_radius, sketches)
        #run_along_spline(number_of_construction_planes, planeInput2, crvPath_spline2, planes2, radius, sketches2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



