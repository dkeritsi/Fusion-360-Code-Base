#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def circle_create (sketch, x, y, z, radius):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), radius)
        prof = sketch.profiles.item(0)
        return prof 

def extrude_circle(rootComp , circle_prof, length):
    extrudes = rootComp.features.extrudeFeatures
    extInput = extrudes.createInput(circle_prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
    extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(length))
    extrudes.add(extInput)

def calculate_tight_bounding_box(body, tolerance = 0):
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

def start_sketch_for_box(design):
    sk = design.rootComponent.sketches.add(design.rootComponent.xYConstructionPlane)        
    lines = sk.sketchCurves.sketchLines

    return lines

def full_bound_box_wrapper(body_base, design):
    bndBox = calculate_tight_bounding_box(body_base) 
    create_points_and_connect_lines(bndBox, design)


def create_points_and_connect_lines(bndBox, design):
        lines = start_sketch_for_box(design)
        minXYZ, minXYmaxZ, minXmaxYZ, minXZmaxY, maxXYZ, maxXYminZ, maxXZminY, maxXminYZ = create_points_box(bndBox)
        connect_the_lines(lines, minXYZ, minXYmaxZ, minXZmaxY, minXmaxYZ, maxXYZ, maxXYminZ, maxXZminY, maxXminYZ)

def create_points_box(bndBox):
    minXYZ = bndBox.minPoint
    minXYmaxZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
    minXmaxYZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.maxPoint.z)
    minXZmaxY = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
    maxXYZ = bndBox.maxPoint
    maxXYminZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
    maxXZminY = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
    maxXminYZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.minPoint.z)

    return minXYZ, minXYmaxZ, minXmaxYZ, minXZmaxY, maxXYZ, maxXYminZ, maxXZminY, maxXminYZ

def connect_the_lines(lines, minXYZ, minXYmaxZ, minXZmaxY, minXmaxYZ, maxXYZ, maxXYminZ, maxXZminY, maxXminYZ):
    lines.addByTwoPoints(minXYZ, minXYmaxZ)
    lines.addByTwoPoints(minXYZ, minXZmaxY)
    lines.addByTwoPoints(minXZmaxY, minXmaxYZ)
    lines.addByTwoPoints(minXYmaxZ, minXmaxYZ)
    
    lines.addByTwoPoints(maxXYZ, maxXYminZ)
    lines.addByTwoPoints(maxXYZ, maxXZminY)
    lines.addByTwoPoints(maxXYminZ, maxXminYZ)
    lines.addByTwoPoints(maxXZminY, maxXminYZ)
    
    lines.addByTwoPoints(minXYZ, maxXminYZ)
    lines.addByTwoPoints(minXYmaxZ, maxXZminY)
    lines.addByTwoPoints(minXmaxYZ, maxXYZ)
    lines.addByTwoPoints(minXZmaxY, maxXYminZ)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        #New Sketch on xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #Circle and Extrude Two Times
        circle_prof = circle_create(sketch,0,0,0, 5) 
        extrude_circle(rootComp, circle_prof, 15)

        circle_prof = circle_create(sketch,0,0,15, 7) 
        extrude_circle(rootComp, circle_prof, 5)

        #Create a Bounding Box
        #Call the function to get the tight bounding box.
        ui.messageBox("Select Body")
        selection_object = ui.selectEntity('Select the body.', 'Bodies')

        body_base = adsk.fusion.BRepBody.cast(selection_object.entity)
        
        # Call the function to get the tight bounding box.

        full_bound_box_wrapper(body_base, design)





    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
