import pygame as pg

class Tile:
    def __init__(self, _img, _up = None, _left = None, _down = None, _right = None):
        self.img = _img
        self.up = _up
        self.left = _left
        self.down = _down
        self.right = _right


