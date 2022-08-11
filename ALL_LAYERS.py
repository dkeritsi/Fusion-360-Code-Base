#Fusion360API Python Script
#Author-kantoku
#Description-CreatePlane ClickPoint

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        planes = root.constructionPlanes

        msg = 'Click on the face / End is ESC key'
        skt = None

        while True:
            sel = SelectEnt(ui, msg, 'Faces')
            if sel is None:
                break

            if skt is None:
                skt = root.sketches.add(root.xYConstructionPlane)

            pnt = skt.sketchPoints.add(sel.point)

            InitPlane(planes, sel.entity, pnt)

        ui.messageBox('Done')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def InitPlane(
        plns :adsk.fusion.ConstructionPlanes,
        surf :adsk.fusion.BRepFace,
        pnt :adsk.core.Point3D):

    plnInput = plns.createInput()
    if plnInput.setByTangentAtPoint(surf, pnt):
        plns.add(plnInput)

def SelectEnt(
        ui :adsk.core.UserInterface,
        msg :str, 
        filtter_str :str) -> adsk.core.Selection :

    try:
        selection = ui.selectEntity(msg, filtter_str)
        return selection
    except:
        return None