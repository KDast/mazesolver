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
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_y = cell_size_y
        self.cell_size_x = cell_size_x
        self.win = win
        self.cells = []
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
            
        for i in range(self.num_cols):
            row_list = []
            for j in range(self.num_rows):
                row_list.append(Cell(self.win))
            self.cells.append(row_list)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell( i, j )

    def _draw_cell(self, i, j):
        x1_pos = self.x1 + i * self.cell_size_x
        x2_pos = x1_pos + self.cell_size_x
        y1_pos = self.y1 + j * self.cell_size_y
        y2_pos = y1_pos + self.cell_size_y
        
        self.cells[i][j].draw(x1_pos, y1_pos, x2_pos, y2_pos)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance = self.cells[0][0]
       
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        exit = self.cells[self.num_cols-1][self.num_rows-1]
        exit.has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)

        








       


    


