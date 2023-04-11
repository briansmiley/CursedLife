## Cursed Life

This is a basic exercise in the [Curses](https://docs.python.org/3/howto/curses.html) Python module, implementing Conway's Game of Life in a console display format.

Default launch mode is a randomized grid of live cells, use --draw/-d to draw a custom initial frame.

Command line arguments:

    Modes:
    --draw, -dr: initializes the grid in "draw" mode, allowing moving the cursor to set intial frame
    --glider, -g: places some gliders in hard coded positions
    --random, -r [float]: initializes the grid with [float] proportion of cells randomly active
    --spiral, -sp: initializes grid with a symmetrical spiral shape

    Settings:
    --speed, -s [int]: sets refresh rate to [int]ms (default 75ms)
    --dimensions, -d [int] [int]: sets the height and width of the display grid; defaults to 50 x 100
    --wrap, -w: turns on edge-wrapping, so that cells on the border consider those on the opposite their neighbors
    --stepwise, -sw: makes the grid update only when on keypress (causes --speed to be ignored)


https://user-images.githubusercontent.com/34353764/229634872-6017fcfb-9bdc-4548-836f-b8cb868a6a1c.mov

*Clip of some gliders*



https://user-images.githubusercontent.com/34353764/229634880-8c53168d-5e86-43b8-adc8-0969627b12c4.mov

*Clip of a random grid*
