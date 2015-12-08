class Material:
    __register = {}
    __all = []
    def by_name(name):
        assert(type(name) == str)
        name = name.lower()
        if name in Material.__register:
            return Material.__register[name]
        else:
            raise ValueError('No material with name', name)
    def has_material(name):
        return name in Material.__register
    def __init__(self, dic):
        self.name = dic['name']
        self.color = dic['color']
        self.dic = dic
        if self.name in Material.__register:
            raise ValueError('A material with name {} already exists'.format(self.name))
        else:
            Material.__register[self.name] = self
        
        

from parse import read_materials
#from tweaks import log

for mat in read_materials('./lore/for_robots/materials.txt'):
    a=Material(mat)
    #log(a.name, f='mat.txt')
