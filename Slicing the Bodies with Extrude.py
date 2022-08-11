#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import array as arr

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent

        #####Create Body #####

        #Initalize
        line_array = [0 for i in range(100)] 
        points = [0 for i in range(100)] 

        #New Sketch on xy plane
        sketches = root.sketches
        xyPlane = root.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #Sketch Circle
        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude
        extrudes = root.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        #Extrude Distance
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10))

        #Create the Extrusion
        ext = extrudes.add(extInput)

        #####Create Construction Planes#####

        #create line and construction planes
        lines = sketch.sketchCurves.sketchLines
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        offset_bottom = adsk.core.ValueInput.createByReal(0)
        offset_top = adsk.core.ValueInput.createByReal(.254)
        z_change = 0

        for i in range(10):
            pt1 = adsk.core.Point3D.create(0,0,i)
            #pt2 = adsk.core.Point3D.create(0,0,i+.254)
            #line_array[i] = lines.addByTwoPoints(pt1, pt2)
            #planeInput.setByDistanceOnPath(line_array[i], offset_bottom)
            #bottom_plane = planes.add(planeInput)
            #planeInput.setByDistanceOnPath(line_array[i], offset_top)
            #top_plan = planes.add(planeInput)

            xyPlane = root.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            circles = sketch.sketchCurves.sketchCircles

            circles.addByCenterRadius(pt1, 4)
            #circles.addByCenterRadius(pt2, 4)
            dist = adsk.core.ValueInput.createByReal(.254) 
            prof = sketch.profiles.item(0)
            extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setDistanceExtent(False, dist)
            extrude = extrudes.add(extrudeInput)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))