class Material:
    __register = {}
    def __init__(self, name, color):
        assert(type(name) == str)
        assert(type(color) == str or color == None)
        name = name.lower()
        if color != None: color = color.lower()
        self.name = name
        self.color = color
        if name in Material.__register:
            raise ValueError('A material with name {} already exists'.format(name))
        else:
            Material.__register[name] = self
    def by_name(name):
        assert(type(name) == str)
        name = name.lower()
        if name in Material.__register:
            return Material.__register[name]
        else:
            raise ValueError('No material with name', name)
    def has_material(name):
        return name in Material.__register
        
        
Stone = Material('stone', 'white')
Air = Material('air', 'red')
Water = Material('water', 'blue')
Sand = Material('sand', 'yellow')
Void = Material('void', 'black')
Dirt = Material('dirt', 'brown')
