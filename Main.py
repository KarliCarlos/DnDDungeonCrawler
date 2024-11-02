#############################################
# ONLY EDIT IF YOU KNOW WHAT YOU ARE DOING! #
#############################################
import pygame as pg
import os
from tkinter import filedialog
import json
from Config import *

pg.init()

class Main:
    def __init__(self):

####### CONFIG #######

        self.SIZE = WindowSize
        self.SIDEPANELSIZE = 500
        self.MINIMAPMARGIN = 50
        self.MAPSIZE = MapSize
        self.STARTCOORDS = [int(self.MAPSIZE/2), int(self.MAPSIZE/2)]
        self.EDITMODE = EditMode

####### VARIABLES #######

        if not self.EDITMODE:
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:    
            self.screen = pg.display.set_mode((self.SIZE + self.SIDEPANELSIZE, self.SIZE))
            
        self.clock = pg.time.Clock()

        self.types = [t for t in os.listdir(os.path.join('Tiles'))]
        self.loadedTiles = [[None for _ in os.listdir(os.path.join('Tiles', k))] for k in self.types]

        self.currentType = [0, 0]

        self.map = [[None for _ in range(self.MAPSIZE)] for _ in range(self.MAPSIZE)]
        self.coords = self.STARTCOORDS.copy()

        self.font = pg.font.SysFont("Consolas", 30)

### FUNCTIONS ###

    def reloadTileImg(self, save = True):
        if not self.loadedTiles[self.currentType[0]][self.currentType[1]]: # Wurde das Bild schonmal geladen?
            size = self.screen.get_height()
            self.loadedTiles[self.currentType[0]][self.currentType[1]] = pg.transform.scale(pg.image.load(os.path.join('Tiles', self.types[self.currentType[0]], str(self.currentType[1] + 1) + FileExtension)), (size, size)) #Bild wird geladen
        if save:
            self.map[self.coords[1]][self.coords[0]] = [self.currentType[0], self.currentType[1]] # Img Daten werden in map gespeichert

    def drawCurrentTile(self):
        if not self.map[self.coords[1]][self.coords[0]]: # Wenn noch kein Tile vorhanden -> Neues Tile
            self.currentType = [0, 0]
            self.reloadTileImg()
        imgPointer = self.map[self.coords[1]][self.coords[0]]
        pos = (0, 0) if self.EDITMODE else ((self.screen.get_width() - self.screen.get_height()) / 2, 0)
        self.screen.blit(self.loadedTiles[imgPointer[0]][imgPointer[1]], pos) # Bild wird angezeigt

    def drawMinimap(self):
        rectSize = int((self.SIDEPANELSIZE - self.MINIMAPMARGIN * 2) / self.MAPSIZE) # Tilesize

        for y, yData in enumerate(self.map):
            for x, xData in enumerate(yData):
                if not xData:
                    continue
                if not self.coords == [x, y]:
                    pg.draw.rect(self.screen, '#5E5E5E', (self.SIZE + self.MINIMAPMARGIN + rectSize * x, self.MINIMAPMARGIN + rectSize * y, rectSize, rectSize))
                    if [x, y] == self.STARTCOORDS:
                        pg.draw.rect(self.screen, '#5E8C5E', (self.SIZE + self.MINIMAPMARGIN + rectSize * x, self.MINIMAPMARGIN + rectSize * y, rectSize, rectSize))
                    continue
                
                pg.draw.rect(self.screen, '#F05E5E', (self.SIZE + self.MINIMAPMARGIN + rectSize * x, self.MINIMAPMARGIN + rectSize * y, rectSize, rectSize))

        pg.draw.rect(self.screen, (220, 220, 220), (self.SIZE + self.MINIMAPMARGIN, self.MINIMAPMARGIN, self.SIDEPANELSIZE - self.MINIMAPMARGIN * 2, self.SIDEPANELSIZE - self.MINIMAPMARGIN * 2), 2) # Minimapborder

    def delete(self):
        if not self.coords == self.STARTCOORDS:
            self.map[self.coords[1]][self.coords[0]] = None
            self.coords = self.STARTCOORDS.copy()
        else:
            print('cant delete')

    def save(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension='.json')
        if not file:
            return
        json.dump([self.STARTCOORDS, self.map], file)
        file.close()

    def load(self):
        file = filedialog.askopenfile(defaultextension='.json')
        if not file:
            return
        data = json.load(file)
        self.map = data[1]
        self.STARTCOORDS = data[0]
        file.close()

        for i in self.map:
            for j in i:
                if not j:
                    continue
                self.currentType = j
                self.reloadTileImg(False)

        self.MAPSIZE = len(self.map)

        self.coords = self.STARTCOORDS.copy()

    def text(self, text):
        return self.font.render(text, True, (220, 220, 220))

    def drawInfo(self):
        lineSize = 40
        startY = self.SIZE - 340
        self.screen.blit(self.text(f"Current Tile: {self.types[self.currentType[0]]} | {self.currentType[1]}"), (self.SIZE + self.MINIMAPMARGIN, self.SIZE / 2))

        self.screen.blit(self.text("Hotkeys:"), (self.SIZE + self.MINIMAPMARGIN, startY))
        self.screen.blit(self.text("←↑↓→  Move around"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize))
        self.screen.blit(self.text("A|D   Change tile"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 2))
        self.screen.blit(self.text("W|S   Change tile type"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 3))
        self.screen.blit(self.text("ENTER Save"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 4))
        self.screen.blit(self.text("L     Load"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 5))
        self.screen.blit(self.text("DEL   Delete Tile"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 6))
        self.screen.blit(self.text("F     Set Starting-Point"), (self.SIZE + self.MINIMAPMARGIN, startY + lineSize * 7))

### GAME LOOP ###

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()
                if e.type == pg.KEYUP:
                    if e.key == pg.K_UP:
                        if self.coords[1] > 0:
                            self.coords[1] -= 1
                            if not self.map[self.coords[1]][self.coords[0]] and not self.EDITMODE:
                                self.coords[1] += 1

                    if e.key == pg.K_DOWN:
                        if self.coords[1] < self.MAPSIZE - 1:
                            self.coords[1] += 1
                            if not self.map[self.coords[1]][self.coords[0]] and not self.EDITMODE:
                                self.coords[1] -= 1

                    if e.key == pg.K_LEFT:
                        if self.coords[0] > 0:
                            self.coords[0] -= 1
                            if not self.map[self.coords[1]][self.coords[0]] and not self.EDITMODE:
                                self.coords[0] += 1

                    if e.key == pg.K_RIGHT:
                        if self.coords[0] < self.MAPSIZE - 1:
                            self.coords[0] += 1
                            if not self.map[self.coords[1]][self.coords[0]] and not self.EDITMODE:
                                self.coords[0] -= 1

                    if e.key == pg.K_l:
                        self.load()

                    if self.EDITMODE:
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
                                self.currentType[1] = len(self.loadedTiles[self.currentType[0]]) - 1
                            else:
                                self.currentType[1] -= 1
                            self.reloadTileImg()

                        if e.key == pg.K_d:
                            if self.currentType[1] == len(self.loadedTiles[self.currentType[0]]) - 1:
                                self.currentType[1] = 0
                            else:
                                self.currentType[1] += 1
                            self.reloadTileImg()

                        if e.key == pg.K_RETURN:
                            self.save()

                        if e.key == pg.K_DELETE:
                            self.delete()

                        if e.key == pg.K_f:
                            self.STARTCOORDS = self.coords.copy()
            self.screen.fill('#0c0908')

            self.drawCurrentTile()
            if self.EDITMODE:
                self.drawMinimap()   
                self.drawInfo()

            if self.map[self.coords[1]][self.coords[0]]:
                self.currentType = self.map[self.coords[1]][self.coords[0]].copy()

            pg.display.flip()
            self.clock.tick(30)


### INIT ###

main = Main()
main.run()