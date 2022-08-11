#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def circle_create (sketch, x, y, z, radius):
        circles = sketch.sketchCurves.sketchCircles
        circles.addByCenterRadius(adsk.core.Point3D.create(x,y,z), radius)
        prof = sketch.profiles.item(0)
        return prof 


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
        design = app.activeProduct
        rootComp = design.rootComponent

        number_of_points = 4 #Number of points for Spline
        radius = 2 #Radius for Pipe
        ui.messageBox("Please enter in " + str(number_of_points) + " points for Pipe Spline.")
        points_float = [[0]*3 for i in range (number_of_points)]
        theta = 20

        #Example values include 
        # 0,0,0; 
        # 0, 0, 10; 
        # 3, 0, 14; 
        # 10, 0, 15;

        points_float[0]= [0,0,0]
        points_float[1]= [0,0,10]
        points_float[2]= [-3,0,14]
        points_float[3]= [-10,0,15]

        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
        points = []
        spline = []

        points.append(adsk.core.ObjectCollection.create())
        for i in range (number_of_points):
            points[0].add(adsk.core.Point3D.create(points_float[i][0], points_float[i][1], points_float[i][2]))
        spline.append(sketch.sketchCurves.sketchFittedSplines.add(points[0]))

        ui.messageBox("Construction of Splines Complete.")
      
        #New Sketch on xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        circle_prof = circle_create(sketch, points_float[0][0] ,points_float[0][1], points_float[0][2], radius) #We want to sweep the first sketch which should be the circle

        ui.messageBox("Circle Sketched Complete.")

        # Create a sweep input
        path = rootComp.features.createPath(spline[0])
        sweeps = rootComp.features.sweepFeatures
        sweepInput = sweeps.createInput(circle_prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Create the sweep.
        sweep_feature_object = sweeps.add(sweepInput)
        ui.messageBox("Sweeping Complete based on Circle and Spline Path.")

        #Create a Bounding Box
        #Call the function to get the tight bounding box.
        ui.messageBox("Select Body")
        selection_object = ui.selectEntity('Select the body.', 'Bodies')

        body_base = adsk.fusion.BRepBody.cast(selection_object.entity)
        
        # Call the function to get the tight bounding box.

        bndBox= calculateTightBoundingBox(body_base)

        # Draw the bounding box using a sketch.
        sk = design.rootComponent.sketches.add(design.rootComponent.xYConstructionPlane)        
        lines = sk.sketchCurves.sketchLines
        
        minXYZ = bndBox.minPoint
        top = bndBox.maxPoint.z
        bottom = bndBox.minPoint.z

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

        #Set up Construction Planes along Spline 
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        #Create a Path based on the Spline 
        sketch1 = rootComp.sketches.item(0)
        crvPath_spline = sketch1.sketchCurves.sketchFittedSplines.item(0)
        number_of_construction_planes = 100

        for i in range (number_of_construction_planes):
            # Add construction plane by distance on path based on percentage. We are going to run along the spline 1% each loop
            distance = adsk.core.ValueInput.createByReal(i/number_of_construction_planes) 
            planeInput.setByDistanceOnPath(crvPath_spline, distance)
            plane_i = planes.add(planeInput)

            #Extract features from the construction plane
            plane_object = plane_i.geometry 
            u_vector = plane_object.uDirection
            v_vector = plane_object.vDirection
            cross_product_u_v = u_vector.crossProduct(v_vector)

            #We want the build direction to be equal to the first construction plane 
            if i == 0:
                build_path_normal = cross_product_u_v

            angle_between = cross_product_u_v.angleTo(build_path_normal)

            #ui.messageBox("The angel between is: " + str(math.degrees(angle_between)))

            if math.degrees(angle_between) > theta:
                #Place Sketch at Same Location of Construction Plane
                sketch = sketches.add(plane_i) #Sketch Plane can be passed an object type of Construction Plane
                circles = sketch.sketchCurves.sketchCircles
                circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius*2) #Set <0,0,0> since this coextensive with instant Construction Plane

                #Extrude
                extrudes = rootComp.features.extrudeFeatures
                dist = adsk.core.ValueInput.createByReal(.1) 
                prof = sketch.profiles.item(0)
                extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extrudeInput.setDistanceExtent(False, dist)
                extrudes.add(extrudeInput)

                #After Extruding, now we want to set the build direction EQUAL to the instant construction plane (similar to if i=0)
                build_path_normal = cross_product_u_v
                    
        ui.messageBox("Slicing Body Complete")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))



