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

        #Initalize
        line_array = [0 for i in range(100)] 

        #New Sketch on xy plane
        sketches = root.sketches
        xyPlane = root.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #create line
        lines = sketch.sketchCurves.sketchLines
        points = adsk.core.ObjectCollection.create()
        for i in range(10):
            pt1 = adsk.core.Point3D.create(0,0,i)
            pt2 = adsk.core.Point3D.create(0,0,i+1)
            line_array[i] = lines.addByTwoPoints(pt1, pt2)

        #create construction plane
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        offset = adsk.core.ValueInput.createByReal(1)

        for i in range(10):
            planeInput.setByDistanceOnPath(line_array[i], offset)
            constPlane = planes.add(planeInput)

        

        #points = adsk.core.ObjectCollection.create()

        #pnt = adsk.core.Point3D.create(0,0,0) 
        #normal_vector = adsk.core.Vector3D.create(0,0,1)
        #plane = adsk.core.Plane.create(pnt, normal_vector)

  #      planeInput = root.constructionPlanes.createInput()
  #      planeInput.setByThreePoints(pnt1, pnt2, pnt3)
  #      plane = root.constructionPlanes.add(planeInput)



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
