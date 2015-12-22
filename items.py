'''
    This file holds the whole item system.
    Each item is only described with a set of qualities, this allows anything to be done with ant item.
'''

import materials

class Item:
    reg = set()
    quals = set()
    def __init__(self, dic):
        self.dic = dic
        Item.reg.add(self)
        Item.check_qualities()
    def check_qualities():
        for item in Item.reg:
            for quality in Item.quals:
                if quality[0] not in item.dic:
                    item.dic[quality[0]] = quality[1]
                else:
                    assert(type(item.dic[quality[0]]) == quality[2] or (type(item.dic[quality[0]]) == int and quality[2] == float))
    def add_quality(quality, default_value, kind=object):
        Item.quals.add((quality, default_value, kind))
        Item.check_qualities()
    def add_qualities(*quals):
        for q in quals:
            Item.add_quality(*q)
    def __getitem__(self, q_name):
        return self.dic[q_name]
    def __setitem__(self, q_name, q_value):
        self.dic[q_name] = q_value
    def clone(self):
        return Item(self.dic)
            
Item.add_qualities(
('name', 'nothing', str),
('mass', 0.0, float),   #kilograms
('volume', 0.0, float), #liters
('color', 'black', str),
('sharpness', 0.0, float),
('light', 0, int),
('material', materials.Material.by_name('void'), materials.Material)
)

sword = Item({
    'name': 'THE SWORD',
    'mass': 5,
    'volume': 4,
    'color': 'gray',
    'sharpness': 100,
    'material': materials.Material.by_name('iron')
})
