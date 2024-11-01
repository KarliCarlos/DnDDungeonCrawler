import pygame as pg
import os

import pprint

pg.init()

class Main:
    def __init__(self):

####### CONFIG #######

        self.EDITMODE = True
        self.SIZE = 1024
        self.MAPSIZE = 10

####### VARIABLES #######

        self.screen = pg.display.set_mode((self.SIZE, self.SIZE))
        self.clock = pg.time.Clock()

        self.loadedTiles = {
            "OneWay": [],
            "TwoWay": [],
            "ThreeWay": [],
            "FourWay": [],
            "HallWay": []
        }
        for k,v in self.loadedTiles.items():
            for i in os.listdir(os.path.join('Tiles', k)):
                v.append(None)

        self.currentType = [0, 0]
        self.types = [k for k in self.loadedTiles.keys()]

        self.map = [[None for _ in range(self.MAPSIZE)] for _ in range(self.MAPSIZE)]
        self.coords = [int(self.MAPSIZE/2), int(self.MAPSIZE/2)]

### FUNCTIONS ###

    def reloadTileImg(self):
        if not self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]]: #Wurde das Bild schonmal geladen?
            self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]] = pg.transform.scale(pg.image.load(os.path.join('Tiles', self.types[self.currentType[0]], str(self.currentType[1] + 1) + '.jpg')), (1024, 1024)) #Bild wird geladen
        self.map[self.coords[1]][self.coords[0]] = (self.types[self.currentType[0]], self.currentType[1])

    def drawCurrentTile(self):
        if not self.map[self.coords[1]][self.coords[0]]: #Wenn noch kein Tile vorhanden -> Neues Tile
            self.currentType = [0, 0]
            self.reloadTileImg()
        imgPointer = self.map[self.coords[1]][self.coords[0]]
        self.screen.blit(self.loadedTiles[imgPointer[0]][imgPointer[1]], (0,0)) #Bild wird angezeigt

### GAME LOOP ###

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
                if self.EDITMODE == True:
                    if e.type == pg.KEYUP:
                        ## Change Imgs ##
                        if e.key == pg.K_w:
                            if self.currentType[0] == 4:
                                self.currentType[0] = 0
                            else:
                                self.currentType[0] += 1
                            self.currentType[1] = 0
                            self.reloadTileImg()
                        
                        if e.key == pg.K_s:
                            if self.currentType[0] == 0:
                                self.currentType[0] = 4
                            else:
                                self.currentType[0] -= 1
                            self.currentType[1] = 0
                            self.reloadTileImg()

                        if e.key == pg.K_a:
                            if self.currentType[1] == 0:
                                self.currentType[1] = len(self.loadedTiles[self.types[self.currentType[0]]]) - 1
                            else:
                                self.currentType[1] -= 1
                            self.reloadTileImg()

                        if e.key == pg.K_d:
                            if self.currentType[1] == len(self.loadedTiles[self.types[self.currentType[0]]]) - 1:
                                self.currentType[1] = 0
                            else:
                                self.currentType[1] += 1
                            self.reloadTileImg()

                        ## Change Tiles ##

                        if e.key == pg.K_UP:
                            if self.coords[1] > 0:
                                self.coords[1] -= 1

                        if e.key == pg.K_DOWN:
                            if self.coords[1] < self.MAPSIZE - 1:
                                self.coords[1] += 1

                        if e.key == pg.K_LEFT:
                            if self.coords[0] > 0:
                                self.coords[0] -= 1

                        if e.key == pg.K_RIGHT:
                            if self.coords[0] < self.MAPSIZE - 1:
                                self.coords[0] += 1

            self.drawCurrentTile()        
            pprint.pprint(self.map)

            pg.display.flip()
            self.clock.tick(30)


### INIT ###

main = Main()
main.run()
