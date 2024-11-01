import pygame as pg
from Tile import Tile
import os

pg.init()

class Main:
    def __init__(self):

####### CONFIG #######

        self.EDITMODE = True
        self.SIZE = 1024

####### VARIABLES #######

        self.screen = pg.display.set_mode((self.SIZE, self.SIZE))
        self.clock = pg.time.Clock()

        self.currentTile = None

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


### FUNCTIONS ###

    def createTile(self):
        self.currentType = [0, 0]
        self.currentTile = Tile(self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]])

    def reloadTileImg(self):
        if not self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]]:
            self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]] = pg.transform.scale(pg.image.load(os.path.join('Tiles', self.types[self.currentType[0]], str(self.currentType[1] + 1) + '.jpg')), (1024, 1024))
        self.currentTile.img = self.loadedTiles[self.types[self.currentType[0]]][self.currentType[1]]

    def drawCurrentTile(self):
        if not self.currentTile.img:
            self.reloadTileImg()
        self.screen.blit(self.currentTile.img, (0,0))

### GAME LOOP ###

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
                if self.EDITMODE == True:
                    if e.type == pg.KEYUP:
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

            if self.currentTile == None:
                self.createTile()

            self.drawCurrentTile()            

            pg.display.flip()
            self.clock.tick(30)


### INIT ###

main = Main()
main.run()
