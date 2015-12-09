
from hero import *
#from random import randint
from mapgen import BigMap
from graphics import print, height, width
from creatures import Creature
from parse import read_tiles
ascii = read_tiles()

class Camera: #Keeps track of the hero, tells what part of the field to show
    def __init__(self, w, h, field, actor): #Field is a BigMap object
        assert(isinstance(field, BigMap))
        self.w = w
        self.h = h
        self.field = field
        self.actor = actor
        x, y = field.where_is(self.actor)
        self.x = x - self.w // 2 #starting position
        self.y = y - self.h // 2 #maybe plus, curse the curses
    def update(self):
        x, y = self.field.where_is(self.actor)
        if self.x + self.w // 2 - x not in range(-40, 40):
            self.x = x - self.w // 2
        if self.y + self.h // 2 - y not in range(-10, 10):
            self.y = y - self.h // 2
    def get_screen(self): #returns a tuple of two 2d lists: charmap and colormap
        self.update()
        lightmap = [[self.field.m[y][x].light for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        for c in self.field.get_creatures():
            z = Creature.by_id(c)
            if z:
                zx, zy = self.field.where_is(z)
                if z.light > 0:
                    d = int((z.light - 1)**0.5)
                    for lx in range(max(self.x,zx-d), min(self.x+self.w,zx+d+1)):
                        for ly in range(max(self.y,zy-d), min(self.y+self.h,zy+d+1)):
                            lightmap[ly - self.y][lx - self.x] += int(z.light / (((zx-lx)**2+(zy-ly)**2)+1))
        def symbol_on_cell(cell):
            return str(cell)
        def symbol_on_point(x, y):
            if self.field.visible_by(self.actor, x, y, lightmap[y-self.y][x-self.x]):
                return str(self.field.m[y][x])
            else:
                return ' '
        def color_on_cell(cell):
            if cell.fill.name in ['air', 'void']:
                return cell.floor.color
            else:
                return cell.fill.color
        charmap = [[symbol_on_point(x, y) for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        colormap = [[color_on_cell(self.field.m[y][x]) for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        x, y = self.field.where_is(self.actor)
        for c in self.field.get_creatures():
            z = Creature.by_id(c)
            if z:
                zx, zy = self.field.where_is(z)
                if ((zy - self.y) in range(height)) and ((zx - self.x) in range(width)):
                    if self.field.visible_by(self.actor, zx, zy, lightmap[zy-self.y][zx-self.x]):
                        charmap[zy - self.y][zx - self.x] = z.get_symbol()
                        colormap[zy - self.y][zx - self.x] = 'white'
        x, y = self.field.where_is(self.actor)
        charmap[y - self.y][x - self.x] = self.actor.get_symbol()
        colormap[y - self.y][x - self.x] = 'green'
        return (charmap, colormap)
    def to_local(self, coords):
        x, y = coords
        return (x - self.x, y - self.y)
    def to_global(self, coords):
        x, y = coords
        return (x + self.x, y + self.y)

