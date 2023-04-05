import curses
from curses import wrapper
import time
import numpy as np
import random
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

    #if wrapping, replace -1s with ends and ends+1 with 0
    if args.wrap:
        potential_neighbors = [[cell[0] % h, cell[1] % w] for cell in potential_neighbors]
        return potential_neighbors
    else:
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
    h,w = grid.shape

    #stop if the glider is being drawn outside the grid
    if y >= h-2 or x >= w-2:
        return
    
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
        quit()
    h,w = grid.shape
    for y in range(h):
        for x in range(w):
            #  "#" if cell is 1, "·" if cell is 0
            
            char = ['·','#'][grid[y][x]]
            #curses throws an error when we write the last character, we can ignore it
            try:
                window.addch(y,x,char)
            except:
                pass
def consoleWrite(win, text):
    win.clear()
    win.addstr(text)
    win.refresh()
def editGrid(grid, win):
    y,x = grid.shape[0]//2,grid.shape[1]//2
    console = curses.newwin(1,50,grid.shape[0]+2,0)
    console2 = curses.newwin(1,50,grid.shape[0]+3,0)
    while True:
        consoleWrite(console, f"Console: Y: {y}, X: {x}")
        drawGrid(grid, win)
        win.move(y, x)
        win.refresh()

        key = win.getch()

        #For testing what key is being seen
        consoleWrite(console2, f"{key}")

        #Move cursor x/y on arrow keys
        if key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_RIGHT:
            x += 1
        elif key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_DOWN:
            y += 1

        #Place a live cell on spacebar
        elif key == ord(" "):
            grid[y,x] = 1

        #Stop drawing on enter
        elif key == curses.KEY_ENTER:
            break

def main(scr):
    h,w = tuple(args.dimensions)
    currentFrame = np.zeros((h,w),dtype=int)

    
    
    # draw a blank grid
    scr.clear()
    win = curses.newwin(h,w,1,1)
    win.keypad(True)
    
    
    
    ##Adding initial stuff to the grid
    if args.gliders:
        drawGlider(currentFrame,[2,2],1)
        drawGlider(currentFrame,[20,10])
        drawGlider(currentFrame,[25,34],4)
        drawGlider(currentFrame,[15,79])
        drawGlider(currentFrame,[5,80],2)
        drawGlider(currentFrame,[1,50])

    if args.draw:
        editGrid(currentFrame, win)
    
    if args.random:
        drawNoise(currentFrame, args.random)
    ## /Sandbox

    drawGrid(currentFrame, win)
    win.refresh()

    while True:
        #hide the cursor while game is playing
        curses.curs_set(0)

        #Draw the current frame on the screen
        drawGrid(currentFrame,win)
        win.refresh()

        #Update the frame array one step
        currentFrame = generate_next_grid(currentFrame)

        #If in stepwise mode, wait for keypress
        if args.step:
            win.getkey()
            curses.napms(args.speed)

            #Avoids "buffering" inputs when in stepwise mode
            curses.flushinp()
        else:
            #If not in stepwise mode, wait [speed] ms before iterating
            curses.napms(args.speed)

if __name__ == "__main__":

    #Command line argument parsing
    parser = argparse.ArgumentParser(description="Generate a Game of Life Grid", formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('--draw', '-dr', dest = 'draw', action = 'store_true', help = 'launch in drawing mode to create initial frame')
    parser.add_argument('--speed', '-s', dest = 'speed', type = int, default = 75, help = 'set frame refresh rate in ms (default 75)')
    parser.add_argument("--wrap", "-w", dest = "wrap", action = 'store_true', help = "'wrap' the grid such that cells at the border consider the opposite border adjacent to them; e.g. gliders cross from the bottom of the grid to the top")
    parser.add_argument("--dimensions", "-d", dest = "dimensions", default = [50,100],type = int, nargs = 2, help = "set the dimensions (height width) of the grid (defaults to 50 x 100)")
    parser.add_argument("--stepwise", '-sw', dest = 'step', action = 'store_true', help = 'makes the grid update on keypress instead of at a time interval')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--random', '-r', dest='random', type = float, help = "set a proportion of the grid to randomly activate")
    modes.add_argument('--gliders', '-g', dest='gliders', action = 'store_true', help = 'generate some gliders at hard coded positions')
    args = parser.parse_args()


    wrapper(main)