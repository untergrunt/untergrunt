
from hero import *
#from random import randint
from tiles import *
from mapgen import BigMap
from graphics import print

class Camera: #Keeps track of the hero, tells what part of the field to show
    def __init__(self, w, h, field, actor): #Field is a BigMap object
        assert(isinstance(field, BigMap))
        self.w = w
        self.h = h
        self.field = field
        self.actor = actor
        self.x = self.actor.x - self.w // 2 #starting position
        self.y = self.actor.y - self.h // 2 #maybe plus, curse the curses
        self.m, self.ch_x, self.ch_y = field.get_update(self.x, self.y)
        self.ch_sz = field.sz
    def update(self):
        if self.field.update_needed(self.x, self.y, self.ch_x, self.ch_y):
            self.m, self.ch_x, self.ch_y = self.field.get_update(self.x, self.y)
            print('Got update')
        if self.x + self.w // 2 - self.actor.x not in range(-60, 60):
            self.x = self.actor.x - self.w // 2
        if self.y + self.h // 2 - self.actor.y not in range(-15, 15):
            self.y = self.actor.y - self.h // 2
    def get_screen(self): #returns a tuple of two 2d lists: charmap and colormap
        self.update()
        def symbol_on_cell(cell):
#            if cell.floor.name in ascii:
                if cell.floor.name == 'water':
                    return ascii['water']
                else:
                    return '.'
 #           else:
  #              return '?'
        charmap = [[symbol_on_cell(self.m[x-self.ch_x*self.ch_sz][y-self.ch_y*self.ch_sz]) for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        charmap[self.actor.y - self.y][self.actor.x - self.x] = self.actor.get_symbol()
        colormap = [[self.m[x-self.ch_x*self.ch_sz][y-self.ch_y*self.ch_sz].floor.color for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        colormap[self.actor.y - self.y][self.actor.x - self.x] = 'green'
        return (charmap, colormap)

