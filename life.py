import curses
from curses import wrapper
import time
import numpy as np
import random
import sys
import argparse


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
        if grid[neighbor[0]][neighbor[1]]:
            count += 1
    return count

#Decides if a cell will live or die
def life(grid, y,x):
    n = liveNeighbors(grid,y,x)
    if n == 3:
        return 1
    if n == 2:
        return grid[y][x]
    return 0

#places a glider in the 3x3 area cornered on y,x, 1 goes SE, 2 3 4 go progressively CW
#-->1·#· 2·#· 3### 4###
#    ··#  #··  #··  ··#
#    ###  ###  ·#·  ·#·
def drawGlider(grid,coord,direction = 1):
    y,x = coord[0], coord[1]
    if direction == 1:
        for pair in [[y,x+1],[y+1,x+2],[y+2,x],[y+2,x+1],[y+2,x+2]]:
            grid[pair[0]][pair[1]]=1
    if direction == 2:
        for pair in [[y,x+1],[y+1,x],[y+2,x],[y+2,x+1],[y+2,x+2]]:
            grid[pair[0]][pair[1]]=1
    if direction == 3:
        for pair in [[y,x],[y,x+1],[y,x+2],[y+1,x],[y+2,x+1]]:
            grid[pair[0]][pair[1]]=1
    if direction == 4:
        for pair in [[y,x],[y,x+1],[y,x+2],[y+1,x+2],[y+2,x+1]]:
            grid[pair[0]][pair[1]]=1

#sets random cells all across the grid to positive, "density" sets the proportion of activated cells
def drawNoise(grid,density = .5):
    h,w = grid.shape
    for y in range(h):
        for x in range(w):
            if random.random() < density:
                setCell(grid,[y,x])

#Set a particular coordinate in the grid, default behavior to set to on
def setCell(grid, coord, on = True):
    grid[coord[0]][coord[1]] = [0,1][on]
                
#set arbitrary list of cells to 1
def setCells(grid, coordinates):
    for coord in coordinates:
        setCell(grid,coord)

def generate_next_grid(frame):
    nextFrame = np.empty_like(frame)
    for y,row in enumerate(frame):
        for x,cell in enumerate(row):
            nextFrame[y][x] = life(frame,y,x)
    return nextFrame

#takes a boolean life grid and writes it to a window
def drawGrid(grid,window):
    if grid.shape != window.getmaxyx():
        print("Can't draw grid on missized window")
        return
    h,w = grid.shape
    for y in range(h-1):
        for x in range(w-1):
            #  "#" if cell is 1, "·" if cell is 0
            
            char = ['·','#'][grid[y][x]]
            window.addch(y,x,char)
    
def main(scr):
    h,w = 50,100
    currentFrame = np.zeros((h,w),dtype=int)

    # draw a blank grid
    scr.clear()
    win = curses.newwin(h,w,1,1)
    ##Sandbox adding stuff to the grid
    if args.gliders:
        drawGlider(currentFrame,[2,2],1)
        drawGlider(currentFrame,[20,10])
        drawGlider(currentFrame,[25,34],4)
        drawGlider(currentFrame,[15,79])
        drawGlider(currentFrame,[5,80],2)
        drawGlider(currentFrame,[1,50])

    if args.random:
        drawNoise(currentFrame, args.random)
    ## /Sandbox

    drawGrid(currentFrame, win)
    win.refresh()

    while True:
        currentFrame = generate_next_grid(currentFrame)
        drawGrid(currentFrame,win)
        win.refresh()

        curses.napms(args.speed)
        # win.getch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Game of Life Grid", formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('--speed', '-s', dest='speed', type = int, default = 75, help = 'set frame refresh rate in ms (default 75)')
    demoGroup = parser.add_mutually_exclusive_group()
    demoGroup.add_argument('--random', '-r', dest='random', type = float, help = "set a proportion of the grid to randomly activate")
    demoGroup.add_argument('--gliders', '-g', dest='gliders', action = 'store_true', help = 'generate some gliders at hard coded positions')
    args = parser.parse_args()
    wrapper(main)