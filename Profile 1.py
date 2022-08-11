#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import array as arr

def circle_create (sketch, root):
        #####Create Body #####
        #Sketch Circle
        #Draw Circle
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), 2)

        #Create Profile of Circle
        prof = sketch.profiles.item(0)

        #Extrude
        extrudes = root.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        #Extrude Distance
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(10))

        #Create the Extrusion
        extrudes.add(extInput)

        return extrudes

def calculateTightBoundingBox(body, tolerance = 0):
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

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent


        #Create Circle and Extrude
        #extrudes = circle_create(sketch, root)        
        extrudes = root.features.extrudeFeatures

        ####Bounding Box###

        # Call the function to get the tight bounding box.
        ui.messageBox("Please Select Body")
        bodySelect = ui.selectEntity('Select the body.', 'Bodies')
        body = adsk.fusion.BRepBody.cast(bodySelect.entity)
        
        # Call the function to get the tight bounding box.

        bndBox= calculateTightBoundingBox(body)
        
        # Draw the bounding box using a sketch.
        sk = des.rootComponent.sketches.add(des.rootComponent.xYConstructionPlane)        
        lines = sk.sketchCurves.sketchLines
        
        minXYZ = bndBox.minPoint
        top = bndBox.maxPoint.z
        bottom = bndBox.minPoint.z

        radius = [abs(bndBox.maxPoint.y), abs(bndBox.minPoint.y), abs(bndBox.maxPoint.x), abs(bndBox.minPoint.x)]
        radius_max = max(radius)

        ui.messageBox("The top is: " + str(top))
        ui.messageBox("The bottom is: " + str(bottom))

        minXYmaxZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
        minXmaxYZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.maxPoint.z)
        minXZmaxY = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
        
        maxXYZ = bndBox.maxPoint
        maxXYminZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
        maxXZminY = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
        maxXminYZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.minPoint.z)

        #Connect the Lines
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

        ui.messageBox("Bounding Box Complete")

        #####Create Construction Planes#####

        #New Sketch on xy plane
        sketches = root.sketches
        xyPlane = root.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        #create line and construction planes
        lines = sketch.sketchCurves.sketchLines

        floating_height = bottom 
        while floating_height < top:
            pt1 = adsk.core.Point3D.create(0,0,floating_height)

            xyPlane = root.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            circles = sketch.sketchCurves.sketchCircles
            circles.addByCenterRadius(pt1, 2*radius_max)#This is not good code but we can always add a rectange later instead of a 2x time circle
            #Please not that a circle with just max radius may not work in all instances.

            dist = adsk.core.ValueInput.createByReal(.1) 
            prof = sketch.profiles.item(0)
            extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setDistanceExtent(False, dist)
            extrudes.add(extrudeInput)

            floating_height = floating_height + 1

        ui.messageBox("Slicing Body Complete")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))