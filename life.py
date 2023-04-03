import curses
from curses import wrapper
import time
import numpy as np

w,h = 100,50
currentFrame = np.array(h * [w * [False]])

#get list of the valid neighbors of a cell (i.e. not outside grid)
def neighbors(grid,y,x):
    h,w = grid.shape
    ret = []
    potential_neighbors = [
        [y-1,x-1],
        [y-1,x],
        [y-1,x+1],
        [y,x-1],
        [y,x+1],
        [y+1,x-1],
        [y+1,x],
        [y+1,x+1], 
    ]
    exceptions = []
    if y == 0:
        exceptions.extend([0,1,2])
    if x == 0:
        exceptions.extend([0,3,5])
    if y == h-1:
        exceptions.extend([5,6,7])
    if x == w-1:
        exceptions.extend([2,4,7])
    for idx, coord in enumerate(potential_neighbors):
        if idx not in exceptions:
            ret.append(coord)
    return ret
    
#count active neighbors of a cell
def liveNeighbors(grid,y,x):
    count = 0
    for neighbor in neighbors(grid,y,x):
        if grid(neighbor[0],neighbor[1]):
            count += 1
    return count

#Decides if a cell will live or die
def life(grid, y,x):
    n = liveNeighbors(grid,y,x)
    if n == 3:
        return True
    if n == 2:
        return grid[y][x]
    return False

def generate_next_grid(frame):
    nextFrame = np.empty_like(frame)
    for y,row in enumerate(frame):
        for x,cell in row:
            nextFrame[y][x] = life(frame,y,x)
    

    
def main():

    #draw a blank grid
    # scr.clear()
    # win = curses.newwin(h,w,1,1)
    # for y in range(h-1):
    #     for x in range(w - 1):
    #         char = ['·','#'][grid[y][x]]
    #         win.addch(y, x, char)
    # win.refresh()


    # win.getkey()

if __name__ == "__main__":
    main()