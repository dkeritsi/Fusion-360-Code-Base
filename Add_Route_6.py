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

def build_matrix(rows, cols):
    matrix = []
    for r in range(0,rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix

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

#Populate Cells for Method which is Always Called, and thus, it is in the Constructor of Grid
def populate_cells(x_row_grid_length, y_column_grid_length, sketchPoints, sketchLines, matrix_cell_centers, sketch_lines_draw_perimeter_per_cell, matrix_cell_instances):

        for x in range(0, x_row_grid_length):
            for y in range (0, y_column_grid_length):
                current_cell_instance = Cell(x, y, 0, 1, sketchPoints, sketchLines)
                matrix_cell_centers[x][y] = current_cell_instance.center_point
                matrix_cell_instances[x][y] = Cell(x,y,0,1,sketchPoints, sketchLines) 
                if(sketch_lines_draw_perimeter_per_cell):
                    current_cell_instance.link_with_sketch(sketchLines)

        return matrix_cell_centers, matrix_cell_instances

class Grid:
    x_row_grid_length = 0
    y_column_grid_length = 0
    sketchPoints = 0
    sketchLines = 0
    sketch_lines_draw = False

    def __init__(self, x_row_grid_length_input, y_row_grid_length_input, sketchPoints_input, sketchLines_input, sketch_lines_draw_permimeter_per_cell_input:bool):
        self.x_row_grid_length = x_row_grid_length_input 
        self.y_column_grid_length = y_row_grid_length_input

        self.sketchPoints = sketchPoints_input
        self.sketchLines = sketchLines_input
        self.sketch_lines_draw_perimeter_per_cell= sketch_lines_draw_permimeter_per_cell_input

        #Initialize the Matrix of Cell Instances
        cell_instance_center_point = Cell(0,0,0,0, self.sketchPoints, self.sketchLines).center_point
        self.matrix_cell_centers = build_matrix(self.x_row_grid_length, self.y_column_grid_length)
        self.matrix_cell_instances = build_matrix(self.x_row_grid_length, self.y_column_grid_length)

        #Always Populate Cells for Instance of Grid. 
        self.matrix_cell_centers, self.matrix_cell_instances = populate_cells(self.x_row_grid_length, self.y_column_grid_length, self.sketchPoints, self.sketchLines, self.matrix_cell_centers, self.sketch_lines_draw_perimeter_per_cell, self.matrix_cell_instances)


    def link_cells(self, second_point, first_point, sketchLines):
        sketchLines.addByTwoPoints(second_point, first_point)
    
    def peano_curve(self, sketchLines):
        for x in range(0, self.x_row_grid_length):
            for y in range (0, self.y_column_grid_length):
                self.link_cells(self.matrix_cell_instances[x][y+1].center_point, self.matrix_cell_instances[x][y].center_point, sketchLines)
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
        x_row_grid_length = 3 
        y_column_grid_length = 10 

        grid_instance = Grid(x_row_grid_length, y_column_grid_length, sketchPoints, sketchLines, sketch_lines_draw_permimeter_per_cell_input = False)
        grid_instance.peano_curve(sketchLines)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))