#Author- Dennis Keritsis
#Description- Opto. Alg. the code outlines a 2D grid with center points
#New code changes adds the Cell Class with a method of linking

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

def create_square_cell(center_x, center_y, center_z, offset, sketchPoints, sketchLines):

    #add center point
    sketchPoint = add_point(center_x, center_y, center_z, sketchPoints)

    #add edge nodes
    pt0 = add_point(center_x+(offset/2), center_y+(offset/2), center_z, sketchPoints)
    pt1 = add_point(center_x+(offset/2), center_y-(offset/2), center_z, sketchPoints)
    pt2 = add_point(center_x-(offset/2), center_y-(offset/2), center_z, sketchPoints)
    pt3 = add_point(center_x-(offset/2), center_y+(offset/2), center_z, sketchPoints)

    return sketchPoint, pt0, pt1, pt2, pt3

class Cell:
    center_point = 0
    pt0 = 0
    pt1 = 0
    pt2 = 0
    pt3 = 0

    def __init__(self, x, y, z, offset, sketchPoints, sketchLines):
        self.center_point, self.pt0, self.pt1, self.pt2, self.pt3 = create_square_cell(x, y, z, offset, sketchPoints,sketchLines)

    def link_with_sketch(self, sketchLines):
        sketchLines.addByTwoPoints(self.pt0, self.pt1)
        sketchLines.addByTwoPoints(self.pt1, self.pt2)
        sketchLines.addByTwoPoints(self.pt2, self.pt3)
        sketchLines.addByTwoPoints(self.pt3, self.pt0)

class Grid:
    row_column_grid_length = 0
    sketchPoints = 0
    sketchLines = 0
    sketch_lines_draw = False 

    def __init__(self, row_column_grid_length_input, sketchPoints_input, sketchLines_input, sketch_lines_draw_input:bool):
        self.row_column_grid_length = row_column_grid_length_input
        self.sketchPoints = sketchPoints_input
        self.sketchLines = sketchLines_input
        self.sketch_lines_draw = sketch_lines_draw_input

    #def populate_cells(self, row_column_grid_length, sketchPoints, sketchLines, sketch_lines_draw:bool):
    def populate_cells(self):
        for x in range(0, self.row_column_grid_length):
            for y in range (0, self.row_column_grid_length):
                current_cell = Cell(x, y, 0, 1, self.sketchPoints, self.sketchLines)
                if(self.sketch_lines_draw):
                    current_cell.link_with_sketch(self.sketchLines) 

    def peano_curve(self):

        pass

    def z_curve(self):
        pass

    def countour_para_curve(self):
        pass

    def mass_curve(self):
        pass

    def hilbert_curve(self):
        pass

    def fermat_spiral_curve(self):
        pass

    def fermat_spiral_curve_2(self):
        pass


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        #Object Collections
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        sketchLines = sketch.sketchCurves.sketchLines
        sketchPoints = sketch.sketchPoints
        points = adsk.core.ObjectCollection.create()

        #Variables for Grid
        row_column_grid_length = 5

        grid_instance = Grid(row_column_grid_length, sketchPoints, sketchLines, True)
        grid_instance.populate_cells()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))