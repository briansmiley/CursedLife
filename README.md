## Cursed Life

This is a basic exercise in the Curses Python module, implementing Conway's Game of Life in a console display format.

Currently includes functions to draw a random grid of active cells, and a drawGlider function with 4 direction options!

Command line arguments:

    --glider, -g: places some gliders in hard coded positions
    --random, -r [float]: initializes the grid with [float] proportion of cells randomly active
    --speed, -s [int]: sets refresh rate to [int]ms (default 75ms)
    --dimensions, -d [int] [int]: sets the height and width of the display grid; defaults to 50 x 100
    --wrap, -w: turns on edge-wrapping, so that cells on the border consider those on the opposite their neighbors
    --stepwise: makes the grid update only when on keypress (causes --speed to be ignored)


https://user-images.githubusercontent.com/34353764/229634872-6017fcfb-9bdc-4548-836f-b8cb868a6a1c.mov

*Clip of some gliders*



https://user-images.githubusercontent.com/34353764/229634880-8c53168d-5e86-43b8-adc8-0969627b12c4.mov

*Clip of a random grid*
