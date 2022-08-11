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

#Object Collections
xyPlane = rootComp.xYConstructionPlane
sketch = sketches.add(xyPlane)
sketchLines = sketch.sketchCurves.sketchLines
sketchPoints = sketch.sketchPoints

def build_matrix(rows, cols):
    matrix = []
    for r in range(0,rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix

def add_point(x, y, z):
    point = adsk.core.Point3D.create(x,y,z)
    added_point = sketchPoints.add(point)

    return added_point 

def create_square_cell(center_x, center_y, center_z, offset):

    #add center point
    pt_center = add_point(center_x, center_y, center_z)

    #add edge nodes
    pt0 = add_point(center_x+(offset/2), center_y+(offset/2), center_z)
    pt1 = add_point(center_x+(offset/2), center_y-(offset/2), center_z)
    pt2 = add_point(center_x-(offset/2), center_y-(offset/2), center_z)
    pt3 = add_point(center_x-(offset/2), center_y+(offset/2), center_z)

    return pt_center, pt0, pt1, pt2, pt3

class Cell:
    center_point = 0
    pt0 = 0
    pt1 = 0
    pt2 = 0
    pt3 = 0

    def __init__(self, x, y, z, offset):
        self.center_point, self.pt0, self.pt1, self.pt2, self.pt3 = create_square_cell(x, y, z, offset)

    def link_with_sketch(self):
        sketchLines.addByTwoPoints(self.pt0, self.pt1)
        sketchLines.addByTwoPoints(self.pt1, self.pt2)
        sketchLines.addByTwoPoints(self.pt2, self.pt3)
        sketchLines.addByTwoPoints(self.pt3, self.pt0)

#Populate Cells for Method which is Always Called, and thus, it is in the Constructor of Grid
def populate_cells(x_row_grid_length, y_column_grid_length, sketch_lines_draw_perimeter_per_cell, matrix_cell_instances):

        for x in range(0, x_row_grid_length):
            for y in range (0, y_column_grid_length):
                matrix_cell_instances[x][y] = Cell(x, y, 0, 1) 
                if(sketch_lines_draw_perimeter_per_cell):
                    matrix_cell_instances[x][y].link_with_sketch()

        return matrix_cell_instances

class Grid:
    x_row_grid_length = 0
    y_column_grid_length = 0
    sketch_lines_draw_perimeter_per_cell = False

    def __init__(self, x_row_grid_length_input, y_row_grid_length_input, sketch_lines_draw_permimeter_per_cell_input:bool):
        self.x_row_grid_length = x_row_grid_length_input 
        self.y_column_grid_length = y_row_grid_length_input
        self.sketch_lines_draw_perimeter_per_cell= sketch_lines_draw_permimeter_per_cell_input

        #Initialize the Matrix of Cell Instances
        cell_instance_center_point = Cell(0,0,0,0).center_point
        self.matrix_cell_instances = build_matrix(self.x_row_grid_length, self.y_column_grid_length)

        #Always Populate Cells for Instance of Grid. 
        self.matrix_cell_instances = populate_cells(self.x_row_grid_length, self.y_column_grid_length, self.sketch_lines_draw_perimeter_per_cell, self.matrix_cell_instances)


    def link_cells(self, second_point, first_point):
        sketchLines.addByTwoPoints(second_point, first_point)
    
    def perimeter(self):

        pass

    #PRINTING ROUTES
    def peano_curve(self):
        for x in range(0, self.x_row_grid_length):
            for y in range (0, self.y_column_grid_length-1):
                self.link_cells(self.matrix_cell_instances[x][y+1].center_point, self.matrix_cell_instances[x][y].center_point)

            if (x < self.x_row_grid_length-1):
                if(x % 2 == 0):
                    self.link_cells(self.matrix_cell_instances[x+1][self.y_column_grid_length-1].center_point, self.matrix_cell_instances[x][self.y_column_grid_length-1].center_point)
                else:
                    self.link_cells(self.matrix_cell_instances[x+1][0].center_point, self.matrix_cell_instances[x][0].center_point)

    def andrew_curve_zig_zag(self):
        for x in range(0, self.x_row_grid_length):
            for y in range (0, self.y_column_grid_length):
                if(x % 2 == 0):
                    self.link_cells(self.matrix_cell_instances[x][y].pt2, self.matrix_cell_instances[x][y].pt0)
                else:
                    self.link_cells(self.matrix_cell_instances[x][y].pt3, self.matrix_cell_instances[x][y].pt1)

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

        #Variables for Grid
        x_row_grid_length = 7 
        y_column_grid_length = 10 

        grid_instance = Grid(x_row_grid_length, y_column_grid_length, sketch_lines_draw_permimeter_per_cell_input = False)
        grid_instance.peano_curve()
        #grid_instance.andrew_curve_zig_zag()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))