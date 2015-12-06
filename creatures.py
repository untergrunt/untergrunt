
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
        self.dic = dic
        

Stats.init_class()

class Race:
    def __init__(self, racename, symbol):
        assert(type(racename) == str)
        assert(type(symbol) == str)
        assert(len(symbol) == 1)
        self.name = racename
        self.symbol = symbol
    def set_stats(self, stats):
        assert(type(stats) == Stats)
        self.stats = stats

human_race = Race('human', 'h')
goblin_race = Race('goblin', 'g')
dwarven_race = Race('dwarf', 'd')

class Creature:
    symbol = None
    __max_id = 0
    def __init__(self, race, name, stats=None):
        if stats == None:
            stats = race.stats
        assert(isinstance(race, Race))
        assert(type(name) == str)
        self.race = race
        self.name = name
        Creature.__max_id += 1
        self.id = Creature.__max_id
    def get_symbol(self):
        return self.symbol if self.symbol != None else self.race.symbol
    def can_pass_through(self, cell):
        if cell.floor.name not in ['sand', 'stone', 'dirt']: return False
        if cell.fill.name not in ['air', 'void']: return False
        return True
        
        
        
        
        
        
        
        
'''                                 RACE STATS                      '''

human_stats = Stats({
    'CHR': 10,
    'STR': 10,
    'INT': 10,
    'LCK': 10,
    'FCS': 10,
    'WPR': 10,
    'DXT': 10
})
human_race.set_stats(human_stats)   
goblin_race.set_stats(human_stats) 
dwarven_race.set_stats(human_stats) 
        
        
        
     
        
        
        
        
