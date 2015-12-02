import materials
from hero import *
from random import randint

class Cell: #Stores data about one cell
    floor = materials.Stone
    fill = materials.Air
    def __init__(self, floor=None, fill=None):
        if floor == None: floor = Cell.floor
        if fill == None: fill = Cell.fill
        self.floor = floor
        self.fill = fill
        self.symbol = ['+', '.'][randint(0,1)]
    
class Camera: #Keeps track of the hero, tells what part of the field to show
    def __init__(self, w, h, field, actor):
        self.w = w
        self.h = h
        self.field = field
        self.actor = actor
        self.x = self.actor.x - self.w // 2 #starting position
        self.y = self.actor.y - self.h // 2 #maybe plus, curse the curses
    def update(self):
        if self.x + self.w // 2 - self.actor.x not in range(-60, 60):
            self.x = self.actor.x - self.w // 2
        if self.y + self.h // 2 - self.actor.y not in range(-15, 15):
            self.y = self.actor.y - self.h // 2
    def get_screen(self): #returns a tuple of two 2d lists: charmap and colormap
        self.update()
        charmap = [[self.field[x][y].symbol for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        charmap[self.actor.y - self.y][self.actor.x - self.x] = '@'
        colormap = [[self.field[x][y].floor.color for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        return (charmap, colormap)

