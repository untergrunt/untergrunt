from random import choice
from tweaks import log
from graphics import MessageBox as MSG

class Mind:
    def __init__(self):
        self.memory = [None] * 100

class AI:
    stuck = True
    def __init__(self, identity):
        self.who = identity
        self.mind = Mind()
    def act(self, circumstances):
        pass
    def memorize(self, slot, info):
        self.mind.memory[slot] = info
    def forget(self, slot):
        self.mind.memory[slot] = None
    def knows(self, slot):
        return self.mind.memory[slot] != None
    def recall(self, slot):
        return self.mind.memory[slot]
    def decrease(self, slot, points=1):
        self.mind.memory[slot] -= points
    def increase(self, slot, points=1):
        self.mind.memory[slot] += points
           
           
class idiot_AI(AI):
    def act(self, circumstances, Time):
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
            
class idiotic_seeker_AI(AI):
    def act(self, circumstances, Time):
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        x, y = circumstances.where_is(self.who)
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        hx, hy = circumstances.where_is(circumstances.get_hero())
        dx, dy = hx - x, hy - y
        if dx > 0 and r:
            circumstances.move_creature(self.who, 1, 0)
        elif dx < 0 and l:
            circumstances.move_creature(self.who, -1, 0)
        elif dy > 0 and d:
            circumstances.move_creature(self.who, 0, 1)
        elif dy < 0 and u:
            circumstances.move_creature(self.who, 0, -1)
            
class random_AI(AI):
    def act(self, circumstances, Time):
        x, y = choice(((0,1),(1,0),(0,-1),(-1,0)))
        circumstances.move_creature(self.who, x, y)
        log(self.who.get_stat('SPD'))
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        
class seeker_AI(AI):
    def act(self, circumstances, Time):
        self.stuck = False
        h = circumstances.get_hero()
        hx, hy = circumstances.where_is(h)
        x, y = circumstances.where_is(self.who)
        if circumstances.visible_by(self.who, hx, hy):
            self.memorize(0, (hx, hy))
            self.memorize(1,(hx - x, hy - y))
            self.memorize(2, 20)
            if self.who.light == 10000:
                self.who.light = 5
                MSG.pop('You hear someone whisper: "W-h-h-e s-s-see the hobbitses-s-s..."')
        elif self.knows(0):
            hx, hy = self.recall(0)
            if (hx, hy) == (x, y):
                self.forget(0)
        elif self.knows(1) and self.recall(2) > 0:
            hx, hy = self.recall(1)
            self.decrease(2)
            hx += x
            hy += y
        else:
            hx, hy = x, y
            if self.who.light != 10000:
                self.who.light = 10000
                MSG.pop('You see a flash of light')
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        dx, dy = hx - x, hy - y
        if abs(dx)>abs(dy):
            if dx > 0 and r:
                circumstances.move_creature(self.who, 1, 0)
            elif dx < 0 and l:
                circumstances.move_creature(self.who, -1, 0)
        else:
            if dy > 0 and d:
                circumstances.move_creature(self.who, 0, 1)
            elif dy < 0 and u:
                circumstances.move_creature(self.who, 0, -1)
        
        
        
        
        
        
        
        
        
        
