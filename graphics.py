from tkinter import Tk, BOTH, Canvas
import random
import time

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("mazesolver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__on = False
        self.__root.protocol = ("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.__on = True
        while self.__on:
            self.redraw()
        print("window closed...")
    

    def close(self):
        self.__on = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, y, x):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=4)

    
class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.win = win
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.visited = False



    def draw(self, x1, y1, x2, y2,):
        if self.win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        top_left = Point(self._x1, self._y1)
        bottom_right = Point(self._x2, self._y2)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        if self.has_left_wall == True:
            left_wall = Line(top_left, bottom_left)
            self.win.draw_line(left_wall, "purple") 
        if self.has_right_wall == True:
            right_wall = Line(top_right, bottom_right)
            self.win.draw_line(right_wall, "purple") 
        if self.has_bottom_wall == True:
            bottom_wall = Line(bottom_left, bottom_right)
            self.win.draw_line(bottom_wall, "purple") 
        if self.has_top_wall == True:
            top_wall = Line(top_left, top_right)
            self.win.draw_line(top_wall, "purple")

        if self.has_left_wall == False:
            left_wall = Line(top_left, bottom_left)
            self.win.draw_line(left_wall, "white") 
        if self.has_right_wall == False:
            right_wall = Line(top_right, bottom_right)
            self.win.draw_line(right_wall, "white") 
        if self.has_bottom_wall == False:
            bottom_wall = Line(bottom_left, bottom_right)
            self.win.draw_line(bottom_wall, "white") 
        if self.has_top_wall == False:
            top_wall = Line(top_left, top_right)
            self.win.draw_line(top_wall, "white") 

    def draw_move(self, to_cell, undo=False):
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, fill_color)
class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed = None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_y = cell_size_y
        self._cell_size_x = cell_size_x
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        if seed != None:
            random.seed(seed)


    def _create_cells(self):
            
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):

        while True:
        
            to_visit = []
            self._cells[i][j].visited = True
            #looks up and down
            if i == 0: #looks at edge
                if self.cells[i+1][j].visited == False:
                    to_visit.append(self.cells[i+1][j])

            if i == (self.num_cols-1): #looks at edge
                if self.cells[i-1][j].visited == False:
                    to_visit.append(self.cells[i-1][j])

            else: #we are not on the edge
                if self.cells[i+1][j].visited == False:
                    to_visit.append(self.cells[i+1][j])
                if self.cells[i-1][j].visited == False:
                    to_visit.append(self.cells[i-1][j])


            #looks left and right
            if j == 0: #looks at edge
                if self.cells[i][j+1].visited == False:
                    to_visit.append(self.cells[i][j+1])

            if j == (self.num_rows-1): #looks at edge
                if self.cells[i][j-1].visited == False:
                    to_visit.append(self.cells[i][j-1])

            else: #we are not on the edge
                if self.cells[i][j+1].visited == False:
                    to_visit.append(self.cells[i][j+1])
                if self.cells[i][j-1].visited == False:
                    to_visit.append(self.cells[i][j-1])

            if len(to_visit) == 0:
                self.cells._draw_cell(i, j)
                return    
            cell_to_visit = to_visit[random.randint(0, len(to_visit)-1)]

            if cell_to_visit._x1 == self.cells[i][j]._x1:
                if cell_to_visit._y1 == self.cells[i][j]._y2:
                    self.cells[i][j].has_bottom_wall = False
                    self._draw_cell(i, j)
                    iterations += 1
                    self._break_walls_r(i+1, j)
                else:
                    self.cells[i][j].has_top_wall = False
                    self._draw_cell(i, j)
                    iterations += 1
                    self._break_walls_r(i-1, j)

            if cell_to_visit._y1 == self.cells[i][j]._y1:
                if cell_to_visit._x1 == self.cells[i][j]._x2:
                    self.cells[i][j].has_right_wall = False
                    self._draw_cell(i, j)
                    iterations += 1
                    self._break_walls_r(i, j+1)
                else:
                    self.cells[i][j].has_left_wall = False
                    self._draw_cell(i, j)
                    iterations += 1
                    self._break_walls_r(i, j-1)



            





        








       


    


