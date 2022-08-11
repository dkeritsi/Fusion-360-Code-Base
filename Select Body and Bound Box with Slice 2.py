#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import array as arr
 
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

        ####Boundign Box###

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
        minXYmaxZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
        minXmaxYZ = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.maxPoint.z)
        minXZmaxY = adsk.core.Point3D.create(bndBox.minPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
        
        maxXYZ = bndBox.maxPoint
        maxXYminZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.maxPoint.y, bndBox.minPoint.z)
        maxXZminY = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.maxPoint.z)
        maxXminYZ = adsk.core.Point3D.create(bndBox.maxPoint.x, bndBox.minPoint.y, bndBox.minPoint.z)
        
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

        #create line and construction planes
        lines = sketch.sketchCurves.sketchLines
        planes = root.constructionPlanes
        planeInput = planes.createInput()
        offset_bottom = adsk.core.ValueInput.createByReal(0)
        offset_top = adsk.core.ValueInput.createByReal(.254)
        z_change = 0

        for i in range(10):
            pt1 = adsk.core.Point3D.create(0,0,i)

            xyPlane = root.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            circles = sketch.sketchCurves.sketchCircles

            circles.addByCenterRadius(pt1, 4)
            dist = adsk.core.ValueInput.createByReal(.254) 
            prof = sketch.profiles.item(0)
            extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extrudeInput.setDistanceExtent(False, dist)
            extrude = extrudes.add(extrudeInput)

        ui.messageBox("Slicing Body Complete")


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))