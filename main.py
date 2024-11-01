import pygame as pg
from tile import *
import os

pg.init()
screen = pg.display.set_mode((1024, 1024))
clock = pg.time.Clock()

### VARIABLES ###

editMode = True
currentTile = None
currentType = [0, 0]

LoadedTiles = {
    "OneWay": [],
    "TwoWay": [],
    "ThreeWay": [],
    "FourWay": [],
    "HallWay": []
}

Types = [k for k in LoadedTiles.keys()]

for k,v in LoadedTiles.items():
    for i in os.listdir(os.path.join('Tiles', k)):
        v.append(None)


### FUNCTIONS ###

def createTile():
    global currentTile, currentType
    currentType = [0, 0]
    currentTile = Tile(LoadedTiles[Types[currentType[0]]][currentType[1]], None, None, None, None)

def reloadTileImg():
    global currentTile, currentType

    if not LoadedTiles[Types[currentType[0]]][currentType[1]]:
        LoadedTiles[Types[currentType[0]]][currentType[1]] = pg.transform.scale(pg.image.load(os.path.join('Tiles', Types[currentType[0]], str(currentType[1] + 1) + '.jpg')), (1024, 1024))
    currentTile.img = LoadedTiles[Types[currentType[0]]][currentType[1]]

def drawCurrentTile():
    global currentTile
    if not currentTile.img:
        reloadTileImg()
    screen.blit(currentTile.img, (0,0))

### GAME LOOP ###

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        if editMode == True:
            if e.type == pg.KEYUP:
                if e.key == pg.K_w:
                    if currentType[0] == 4:
                        currentType[0] = 0
                    else:
                        currentType[0] += 1
                    currentType[1] = 0
                    reloadTileImg()
                
                if e.key == pg.K_s:
                    if currentType[0] == 0:
                        currentType[0] = 4
                    else:
                        currentType[0] -= 1
                    currentType[1] = 0
                    reloadTileImg()

                if e.key == pg.K_a:
                    if currentType[1] == 0:
                        currentType[1] = len(LoadedTiles[Types[currentType[0]]]) - 1
                    else:
                        currentType[1] -= 1
                    reloadTileImg()

                if e.key == pg.K_d:
                    if currentType[1] == len(LoadedTiles[Types[currentType[0]]]) - 1:
                        currentType[1] = 0
                    else:
                        currentType[1] += 1
                    reloadTileImg()

    screen.fill("grey")

    if currentTile == None:
        createTile()

    drawCurrentTile()            

    pg.display.flip()
    clock.tick(30)