class Race:
    def __init__(self, racename, symbol):
        assert(type(racename) == str)
        assert(type(symbol) == str)
        assert(len(symbol) == 1)
        self.name = racename
        self.symbol = symbol
    def set_stats(self, stats):
        assert(type(stats) == dict)
        self.stats = stats

human_race = Race('human', 'h')
goblin_race = Race('goblin', 'g')

class Creature:
    x, y = None, None
    symbol = None
    def __init__(self, race, name):
        assert(isinstance(race, Race))
        assert(type(name) == str)
        self.race = race
        self.name = name
    def locate(self, x, y):
        assert(self.x == None and self.y == None)
        self.x = x
        self.y = y
    def get_symbol(self):
        return self.symbol if self.symbol != None else self.race.symbol
        
