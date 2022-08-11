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
        #points = [0 for i in range(100)] 
        circles_array = [0 for i in range(100)] 
        construction_plane_array = [0 for i in range(100)] 
        add_layer = .254
        height_of_body = 10
        vec_z = adsk.core.Vector3D.create(0,0,1)
        vec_x = adsk.core.Vector3D.create(1,0,0)
        vec_y = adsk.core.Vector3D.create(0,1,0)
        ORIGIN = adsk.core.Point3D.create(0,0,0)

        #New Sketch on xy plane
        sketches = root.sketches
        xyPlane = root.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #Sketch Circle
        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        #circles_array[0] = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)
        first_circle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude
        extrudes = root.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        #Extrude Distance
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height_of_body))

        #Create the Extrusion
        ext = extrudes.add(extInput)

        #####Create Construction Planes#####

        #create line and construction planes
        lines = sketch.sketchCurves.sketchLines
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        offset = adsk.core.ValueInput.createByReal(add_layer)
        pnt = adsk.core.Point3D.create(0,0,0)
        #vec_test = adsk.core.Vector3D.create(1,1,1)

        increment = 0 
        #for i in range(10):
            #pt1 = adsk.core.Point3D.create(0,0,increment)
            #pt2 = adsk.core.Point3D.create(0,0,increment + add_layer)
            #Each Addative Layer is .245 mm or 1/100 of an inch
            #line_array[i] = lines.addByTwoPoints(pt1, pt2)
        pln3d = adsk.core.Plane.create(pnt, vec_z)
            #planeInput.setByDistanceOnPath(line_array[i], offset)
        planeInput.setByPlane(pln3d)
            #construction_plane_array[i] = planes.add(planeInput)
        des.designType = adsk.fusion.DesignTypes.DirectDesignType 
        pln = planes.add(planeInput)
        des.designType = adsk.fusion.DesignTypes.ParametricDesignType
            #circles_array[i] = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,increment+add_layer), 4)
            #increment = increment + add_layer


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
