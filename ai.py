from random import choice

class AI:
    def __init__(self, identity):
        self.who = identity
    def act(self, circumstances):
        pass
           
           
class goblin_AI(AI):
    def act(self, circumstances):
        x, y = choice(((0,1),(1,0),(0,-1),(-1,0)))
        circumstances.move_creature(self.who, x, y)
