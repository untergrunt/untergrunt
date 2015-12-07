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
        '''x, y = choice(((0,1),(1,0),(0,-1),(-1,0)))
        circumstances.move_creature(self.who, x, y)
        log(self.who.get_stat('SPD'))'''
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        x, y = circumstances.where_is(self.who)
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        if all((l, r, u, d)) or ((not l) and d):
            circumstances.move_creature(self.who, 0, 1)
        elif (not d) and r:
            circumstances.move_creature(self.who, 1, 0)
        elif (not r) and u:
            circumstances.move_creature(self.who, 0, -1)
        elif (not u) and l:
            circumstances.move_creature(self.who, -1, 0)
