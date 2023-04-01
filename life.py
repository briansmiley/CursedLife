import curses
from curses import wrapper
import time
import numpy

w,h = 10,10
grid = numpy.array(h * [w * ['·']])

#get the valid neighbors of a cell
def neighbors(cell):
    pass
    
#count active neighbors of a cell
def countNeighbors(cell):
    pass

def main(scr):
    scr.clear()
    win = curses.newwin(h,w,1,1)
    for y in range(h-1):
        for x in range(w - 1):
            win.addch(y, x, grid[y][x])
    win.refresh()
    win.getkey()

if __name__ == "__main__":
    wrapper(main)