#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)


        design = app.activeProduct
        rootComp = design.rootComponent
        planes = rootComp.constructionPlanes
        planeInput = planes.createInput()

        point = adsk.core.Point3D.create(0,0,0)
        normal = adsk.core.Vector3D.create(0,0,1)
        
        pln3d = adsk.core.Plane.create(point, normal)
        planeInput.setByPlane(pln3d)
        plane_valid = pln3d.isValid
        normal = pln3d.normal
        origin = pln3d.origin

        pln3d.origin = adsk.core.Point3D.create(10,1,1)
        pln3d.normal = adsk.core.Vector3D.create(1,1,1)

        ui.messageBox("This is the plane property of isValid " + str(plane_valid))
        ui.messageBox("This is the plane property of normal" + str(normal))
        ui.messageBox("This is the plane property of origin" + str(origin))

        design.designType = adsk.fusion.DesignTypes.DirectDesignType
        plane_i = planes.add(planeInput)

        plane_object = plane_i.geometry
        u_vector = plane_object.uDirection
        v_vector = plane_object.vDirection
        cross_product_u_v = u_vector.crossProduct(v_vector)

        string = "This is the location of the u_vector" +"X = "+str(u_vector.x)+ "  Y = " + str(u_vector.y) + "  Z = "+str(u_vector.z) + '\n' 
        string2 = "This is the length of the u_vector is:" + str(u_vector.length) + '\n' 
        string3 = "This is the location of the v_vector" +"X = "+str(v_vector.x)+ "  Y = " + str(v_vector.y) + "  Z = "+str(v_vector.z) + '\n' 
        string4 = "This is the length of the v_vector is:" + str(v_vector.length) + '\n' 
        string5 = "The cross product of u and v is:" +"X = "+str(cross_product_u_v.x)+ "  Y = " + str(cross_product_u_v.y) + "  Z = "+str(cross_product_u_v.z)
        string_last = string + string2 +string3 + string4 +string5


        ui.messageBox(string_last)
  



    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
