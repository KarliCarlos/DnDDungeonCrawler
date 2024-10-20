import pygame as pg
from tile import *

pg.init()
screen = pg.display.set_mode((2560, 1440))
clock = pg.time.Clock()

### VARIABLES ###

currentTile = None

### FUNCTIONS ###

def createTile():
    currentTile = Tile("", None, None, None, None)
#    editTile()

#def editTile():a


### GAME LOOP ###

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill("purple")
    if currentTile == None:
        createTile()

    pg.display.flip()

    clock.tick(30)