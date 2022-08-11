#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def circle_create (sketch, x, y, z):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x, y, z), 2)
        prof = sketch.profiles.item(0)
        return prof 

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        extrudes = rootComp.features.extrudeFeatures

        number_of_points = 4 
        points_float = [[0]*3 for i in range (number_of_points)]

        points_float[0]= [0,0,0]
        points_float[1]= [0,0,10]
        points_float[2]= [5,0,10]
        points_float[3]= [10,0,10]

        #New Sketch on xy plane
        xyPlane = rootComp.xYConstructionPlane
        sketch_xy = sketches.add(xyPlane)
        circle_prof_xy = circle_create(sketch_xy, points_float[0][0], points_float[0][1], points_float[0][2]) 

        ui.messageBox("Circle Sketched Complete on XY.")

        #New Sketch on yz plane
        yzPlane = rootComp.yZConstructionPlane
        sketch_yz = sketches.add(yzPlane)
        circle_prof_yz = circle_create(sketch_yz, -10, 0, 0)

        ui.messageBox("Circle Sketched Complete on YZ.")

        xyPlane = rootComp.xYConstructionPlane
        sketch_xy = sketches.add(xyPlane)
        circle_prof_xy_2 = circle_create(sketch_xy, points_float[3][0], points_float[3][1], points_float[3][2]) 

        ui.messageBox("Circle Sketched Complete on 2nd XY.")

        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = []

        points.append(adsk.core.ObjectCollection.create())
        for i in range (number_of_points-1):
            pt1 = adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2])
            pt2 = adsk.core.Point3D.create(points_float[i+1][0], points_float[i+1][1], points_float[i+1][2])
            sketch.sketchCurves.sketchLines.addByTwoPoints(pt1, pt2)

        ui.messageBox("Construction of Line Complete.")
      
        distance = adsk.core.ValueInput.createByReal(10)
        extrudes.addSimple(circle_prof_xy, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudes.addSimple(circle_prof_yz, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudes.addSimple(circle_prof_xy_2, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        ui.messageBox("Body Build Complete.")

        distance = adsk.core.ValueInput.createByReal(1000)
        extrudes.addSimple(circle_prof_xy, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudes.addSimple(circle_prof_yz, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)

        ui.messageBox("Cut Complete.")
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
