from random import choice
from tweaks import log

class AI:
    stuck = True
    def __init__(self, identity):
        self.who = identity
    def act(self, circumstances):
        pass
           
           
class goblin_AI(AI):
    def act(self, circumstances, Time):
        x, y = choice(((0,1),(1,0),(0,-1),(-1,0)))
        self.stuck = False
        circumstances.move_creature(self.who, x, y)
        log(self.who.get_stat('SPD'))
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
