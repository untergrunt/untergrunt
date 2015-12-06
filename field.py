import materials
from hero import *
#from random import randint
#from tiles import *
#from mapgen import BigMap

class Cell: #Stores data about one cell
    floor = materials.Stone
    fill = materials.Air
    def __init__(self, floor=None, fill=None):
        if floor == None: floor = Cell.floor
        elif not isinstance(floor, materials.Material):
            if materials.Material.has_material(floor):
                floor = materials.Material.by_name(floor)
            else:
                raise ValueError('Expected a material, got', type(floor))
        if fill == None: fill = Cell.fill
        elif not isinstance(fill, materials.Material):
            if materials.Material.has_material(fill):
                fill = materials.Material.by_name(fill)
            else:
                raise ValueError('Expected a material, got', type(fill))
        self.floor = floor
        self.fill = fill
    def __str__(self):
        if self.fill.name not in ['air', 'void']:
            return '#'
        elif self.floor.name == 'water':
            return '~'
        else:
            return '.'
    

