from materials import Material as mat

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
        self.light = 10
    def __str__(self):
        if self.fill.name not in ['air', 'void']:
            return '#'
        elif self.floor.name == 'water':
            return '~'
        else:
            return '.'
