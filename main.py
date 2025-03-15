from graphics import *


def main():
    win = Window(800, 600)
    c1 = Cell(50, 50, 100, 100, win)
    c1.has_left_wall = False
    c1.draw()         
    win.wait_for_close()


main()

