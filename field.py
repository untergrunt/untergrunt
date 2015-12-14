from materials import Material as mat
from parse import read_statics
from random import choice

class Cell: #Stores data about one cell
    floor = mat.by_name('stone')
    fill = mat.by_name('air')
    def __init__(self, floor=None, fill=None):
        if floor == None: floor = Cell.floor
        elif not isinstance(floor, mat):
            if mat.has_material(floor):
                floor = mat.by_name(floor)
            else:
                raise ValueError('Expected a material, got', type(floor))
        if fill == None: fill = Cell.fill
        elif not isinstance(fill, mat):
            if mat.has_material(fill):
                fill = mat.by_name(fill)
            else:
                raise ValueError('Expected a material, got', type(fill))
        self.floor = floor
        self.fill = fill
        self.statics = None
    def __str__(self):
        if self.fill.name not in ['air', 'void']:
            return '#'
        elif self.floor.name == 'water':
            return '~'
        else:
            return '.'
    def add_static(self, static):
        self.statics.append(static)
        
class Static:
    possible = read_statics()
    def __init__(self, kind, x=None, y=None):
        if (x, y) != (None, None):
            self.x, self.y=  x, y
        self.kind = kind
        dic = [i for i in Static.possible if i['name'] == kind][0]
        if 'color' in dic:
            if type(dic['color']) in (list, tuple):
                self.color = choice(dic['color'])
            else:
                self.color = dic['color']
        else:
            self.color = None
        self.passible = dic['passible']
        self.symbol = dic['symbol']
        if 'light' in dic:
            if type(dic['light']) in (list, tuple, range):
                self.light = choice(dic['light'])
            else:
                self.light = dic['light']
        else:
            self.light = 0
        self.transparent = 'transparent' not in dic or dic['transparent'] == True
            
fire = Static('campfire')
        
        
