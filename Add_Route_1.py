#Author- Dennis Keritsis
#Description- Opto. Alg. the code outlines a 2D grid with center points

import adsk.core, adsk.fusion, adsk.cam, traceback, time

#Global Variables
app = adsk.core.Application.get()
ui  = app.userInterface
design = app.activeProduct
rootComp = design.rootComponent
sketches = rootComp.sketches
sweeps = rootComp.features.sweepFeatures
planes = rootComp.constructionPlanes

def add_point(x, y, z, sketchPoints):
    point = adsk.core.Point3D.create(x,y,z)
    sketchPoint = sketchPoints.add(point)

    return sketchPoint

def create_square_cell_and_connect_lines(center_x, center_y, center_z, offset, sketchPoints, sketchLines):

    #add center point
    sketchPoint = add_point(center_x, center_y, center_z, sketchPoints)

    #add edge nodes
    pt1 = add_point(center_x+(offset/2), center_y+(offset/2), center_z, sketchPoints)
    pt2 = add_point(center_x+(offset/2), center_y-(offset/2), center_z, sketchPoints)
    pt3 = add_point(center_x-(offset/2), center_y-(offset/2), center_z, sketchPoints)
    pt4 = add_point(center_x-(offset/2), center_y+(offset/2), center_z, sketchPoints)

    sketchLines.addByTwoPoints(pt1, pt2)
    sketchLines.addByTwoPoints(pt2, pt3)
    sketchLines.addByTwoPoints(pt3, pt4)
    sketchLines.addByTwoPoints(pt4, pt1)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        sketchLines = sketch.sketchCurves.sketchLines
        sketchPoints = sketch.sketchPoints

        #Create and Object Collection for the points
        points = adsk.core.ObjectCollection.create()

        for x in range(0, 10):
            for y in range (0, 10):
                create_square_cell_and_connect_lines(x, y, 0, 1, sketchPoints, sketchLines)



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
