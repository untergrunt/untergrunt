from ai import *
from tweaks import log

class Stats:
    possible = []
    def init_class():
        I = open('stats.txt')
        for line in I:
            if '#' in line: continue
            long, short, description = line[:-1].split(':')
            Stats.possible += [[long, short, description]]
        I.close()
    def __init__(self, dic):
        assert(set([i[1] for i in Stats.possible]) == set(dic.keys()))
        self.dic = dic.copy()
    def copy(self):
        return Stats(self.dic)
        

Stats.init_class()

class Race:
    def __init__(self, racename, symbol, ai_class):
        assert(type(racename) == str)
        assert(type(symbol) == str)
        assert(len(symbol) == 1)
        self.name = racename
        self.symbol = symbol
        self.ai_class = ai_class
    def set_stats(self, stats):
        assert(type(stats) == Stats)
        self.stats = stats

human_race = Race('human', 'h', random_AI)
goblin_race = Race('goblin', 'g', seeker_AI)
dwarven_race = Race('dwarf', 'd', idiot_AI)

class BodyPart:
    def __init__(self, name, size, functions):
        self.name = name
        self.size = size
        self.functions = functions
        self.health = 100 #100 is excelent, 0 is gone, <50 is a serious malfunction
        #Which functions are vital is decided for each creature depending on its needs
        #Damage is also stored here
    def clone(self):
        return BodyPart(self.name, self.size, self.functions)  #A fully healed copy
    def take_damage(self, dmg):
        assert(dmg >= 0)
        self.health -= dmg
        log(self.name, 'takes', dmg, 'damage', f='log')

heart = BodyPart('heart', '0.5', ['blood pressure'])
brain = BodyPart('brain', '2', ['consciousness', 'perception', 'control'])
skin = BodyPart('skin', '10', ['disease resistance', 'protection'])

class Body:
    def __init__(self, parts, root, connect): #Connect is a list of tuples, each of them contains a pair of
                                              #connected organs from root to skin (e.g. (brain, skull))
        self.parts = [i.clone() for i in parts]
        self.root = root.clone()
        self.connect = connect #A crutch for cloning
        for i in self.parts:
            i.outside = []
            i.inside = []
            for fro,to in connect:
                if i.name == fro.name:
                    i.outside.append(to)
                elif i.name == to.name:
                    i.inside.append(fro)
    def clone(self):
        return Body([i.clone() for i in self.parts], self.root.clone(), self.connect[:])
                
bdy = Body([heart, brain, skin], brain, [(brain, heart), (brain, skin), (heart, skin)])

class Creature:
    symbol = None
    __max_id = 0
    __reg = []
    def __init__(self, race, name, body_template, stats=None, ai=None):
        for i in Creature.__reg:
            if i.name == name:
                raise ValueError()
        if stats == None:
            stats = race.stats
        if ai == None:
            self.AI = race.ai_class(self)
        elif isinstance(ai, type):
            self.AI = ai(self)
        else:
            self.AI = ai
        assert(isinstance(race, Race))
        assert(type(name) == str)
        self.needs = set()
        self.body = body_template.clone()
        for p in self.body.parts:
            self.needs.add(p)
        self.race = race
        self.alive = True
        self.name = name
        Creature.__max_id += 1
        self.id = Creature.__max_id
        Creature.__reg.append(self)
        self.stats = stats
        self.vision = self.stats.dic['VSN']
        self.controlled_by_player = False
        self.light = 0
        self.effects = []
        self.check_health()
    def check_health(self):
        functions = set()
        for p in self.body.parts:
            if p.health <= 0:
                q = [p]
                while q != []:
                    exit()
                    curr, q = q[0], q[1:]
                    for i in curr.outside:
                        if i.inside == [curr] and i not in q:
                            q.append(i)
                    self.body.parts.remove(curr)
                    if curr == self.root:
                        return False
            else:
                log(self.name, p.name, 'is OK, health is', p.health, f='log')
        for p in self.body.parts:
            functions.add(p)
        if functions == self.needs:
            return True
        else:
            self.effects = {}
            for i in self.needs - functions:
                if i == 'vision':
                    self.effects.add('blind')
                elif i == 'consciousness':
                    self.effects.add('unconscious')
                elif i == 'control':
                    return False
                elif i == 'blood pressure':
                    return False
        
    def get_symbol(self):
        return self.symbol if self.symbol != None else self.race.symbol
    def can_pass_through(self, cell):
        if cell.floor.name not in ['sand', 'stone', 'dirt']: return False
        if cell.fill.name not in ['air', 'void']: return False
        if cell.statics != None and [True for i in cell.statics if not i.passible] != []: return False
        return True
    def die(self):
        self.AI = None
#        self.controlled_by_player = False
        self.alive = False
    def where_is(self):
        try:
            return (self.x, self.y)
        except:
            return None
    @property
    def position(self):
        return (self.x, self.y)
    @position.setter
    def position(self, p):
        self.x, self.y = p
    def by_id(ID):
        for i in Creature.__reg:
            if i.id == ID:
                return i
    def get_stat(self, stat):
        if stat in self.stats.dic:
            return self.stats.dic[stat]
        else:
            raise ValueError('No such stat -', stat)
    # INTERACTIONS   
    def open_door(self, d):
        if d.kind != 'closed_door':
            return False
        if self.stats.dic['INT'] < 2:
            return False
        d.kind = 'open_door'
        d.passible = True
        d.symbol = '/'
        d.transparent = True
        return True
    def close_door(self, d):
        if d.kind != 'open_door':
            return False
        if self.stats.dic['INT'] < 2:
            return False
        d.kind = 'closed_door'
        d.passible = False
        d.symbol = '+'
        d.transparent = False
        return True
        
        
        
        
        
        
'''                                 RACE STATS                      '''

human_stats = Stats({
    'CHR': 10,
    'STR': 10,
    'INT': 10,
    'LCK': 10,
    'FCS': 10,
    'WPR': 10,
    'DXT': 10,
    'SPD': 10,
    'VSN': 40
})
human_race.set_stats(human_stats.copy())   
goblin_race.set_stats(human_stats.copy()) 
dwarven_race.set_stats(human_stats.copy()) 
        
        
        
     
        
        
        
        
