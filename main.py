from graphics import *


def main():
    win = Window(800, 600)
    l = Line(Point(50, 50), Point(500, 150))
    win.draw_line(l, "purple")         
    win.wait_for_close()


main()

