# Function to test the calculateTightBoundingBox function.

import adsk.core, adsk.fusion, adsk.cam, traceback

# Calculates a tight bounding box around the input body.  An optional
# tolerance argument is available.  This specificies the tolerance in
# centimeters.  If not provided the best existing display mesh is used.
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
        ui = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        
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
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))