
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
        x, y = field.where_is(self.actor)
        self.x = x - self.w // 2 #starting position
        self.y = y - self.h // 2 #maybe plus, curse the curses
        self.m, self.ch_x, self.ch_y = field.get_update(self.x, self.y)
        self.ch_sz = field.sz
    def update(self):
        if self.field.update_needed(self.x, self.y, self.ch_x, self.ch_y):
            self.m, self.ch_x, self.ch_y = self.field.get_update(self.x, self.y)
            print('Got update')
        x, y = self.field.where_is(self.actor)
        if self.x + self.w // 2 - x not in range(-60, 60):
            self.x = x - self.w // 2
        if self.y + self.h // 2 - y not in range(-15, 15):
            self.y = y - self.h // 2
    def get_screen(self): #returns a tuple of two 2d lists: charmap and colormap
        self.update()
        def symbol_on_cell(cell):
            '''
            if cell.fill.name in ['air', 'void']: #Draw what is on the floor
                if cell.floor.name == 'water':
                    return '~'
                else:
                    return '.'
            else:
                if cell.fill.name == 'stone':
                    return '#'
                else:
                    return '!'
           '''
            return str(cell)
        def color_on_cell(cell):
            if cell.fill.name in ['air', 'void']:
                return cell.floor.color
            else:
                return cell.fill.color
        charmap = [[symbol_on_cell(self.m[x-self.ch_x*self.ch_sz][y-self.ch_y*self.ch_sz]) for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        x, y = self.field.where_is(self.actor)
        charmap[y - self.y][x - self.x] = self.actor.get_symbol()
        colormap = [[color_on_cell(self.m[x-self.ch_x*self.ch_sz][y-self.ch_y*self.ch_sz]) for x in range(self.x, self.x + self.w)] for y in range(self.y, self.y + self.h)]
        colormap[y - self.y][x - self.x] = 'green'
        return (charmap, colormap)

