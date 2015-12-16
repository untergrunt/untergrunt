#This file is Orthodox
from random import choice
from tweaks import log as LOG
from graphics import MessageBox as MSG

log = lambda *x: LOG(*x, f='logs/ai.log')

class Mind:
    '''
        The class stores mental data of  the bot
    '''
    def __init__(self):
        log('New mind')
        self.memory = [None] * 100

class AI:
    '''
        This class represents the bot's brain, using memory and mental background
        as well as the situation around to make decisions
        Every subclass of this class represents a certain strategy. However,
        the same subclass may act diffirently when controlling diffirent creatures.
        Instances of __this__ class should not be created, only these of its subclasses
    '''
    stuck = True
    def __init__(self, identity):
        log('New AI for', identity.name)
        self.who = identity
        self.mind = Mind()
    def ACT(self, circumstances, Time):
        '''
            This function is the heart of the class --
            it defines what the bot is going to do
            An 'empty' soulless bot obviously does not do anything
        '''
        pass
    def act(self, circumstances, Time):
        '''
            This function defines whether the bot can actually do anything,
            particularly, it prevents the dead from doing anything
            This function may be considered a chutch and replaced later
        '''
        if self.who.alive:
            self.ACT(circumstances, Time)
        else:
            pass
    def memorize(self, slot, info):
        '''
            Makes the bot put some <info> into its memory <slot>
        '''
        self.mind.memory[slot] = info
    def forget(self, slot):
        '''
            Makes the bot forget info that is stored in <slot>
        '''
        self.mind.memory[slot] = None
    def knows(self, slot):
        '''
            Provides information about whether the bot knows something that
            should be stored in <slot> or not
        '''
        return self.mind.memory[slot] != None
    def recall(self, slot):
        '''
            Makes the bot remember what he once learned
        '''
        return self.mind.memory[slot]
    def decrease(self, slot, points=1):
        '''
            The bot decreases the counter that is stored in <slot> by <points>
        '''
        self.mind.memory[slot] -= points
    def increase(self, slot, points=1):
        '''
            The bot increases the counter that is stored in <slot> by <points>
        '''
        self.mind.memory[slot] += points
           
           
class idiot_AI(AI):
    '''
        This AI is a total and complete idiot. It simply runs around the room
    '''
    def ACT(self, circumstances, Time):
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        x, y = self.who.position
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        if all((l, r, u, d)) or ((not l) and d):
            circumstances.move_creature(self.who, 0, 1)
            log(self.who.name+'\'s idiotic AI decides to go down')
        elif (not d) and r:
            circumstances.move_creature(self.who, 1, 0)
            log(self.who.name+'\'s idiotic AI decides to go right')
        elif (not r) and u:
            circumstances.move_creature(self.who, 0, -1)
            log(self.who.name+'\'s idiotic AI decides to go up')
        elif (not u) and l:
            circumstances.move_creature(self.who, -1, 0)
            log(self.who.name+'\'s idiotic AI decides to go left')
            
class idiotic_seeker_AI(AI):
    '''
        This AI is not as much of an idiot as the idiot_AI, yet it cannot be any serious threat
        to a hero whose INT is a positive value
    '''
    def ACT(self, circumstances, Time):
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        x, y = self.who.position
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        hx, hy = circumstances.get_hero().position
        dx, dy = hx - x, hy - y
        if dx > 0 and r:
            circumstances.move_creature(self.who, 1, 0)
            log(self.who.name+'\'s idiotic seeker AI decides to go right')
        elif dx < 0 and l:
            circumstances.move_creature(self.who, -1, 0)
            log(self.who.name+'\'s idiotic seeker AI decides to go left')
        elif dy > 0 and d:
            circumstances.move_creature(self.who, 0, 1)
            log(self.who.name+'\'s idiotic seeker AI decides to go down')
        elif dy < 0 and u:
            circumstances.move_creature(self.who, 0, -1)
            log(self.who.name+'\'s idiotic seeker AI decides to go up')
            
class random_AI(AI):
    '''
        This AI makes a step in a random direction every turn
    '''
    def ACT(self, circumstances, Time):
        x, y = choice(((0,1),(1,0),(0,-1),(-1,0)))
        circumstances.move_creature(self.who, x, y)
        log(self.who.name+'\'s random AI decides move by vector ({}, {})'.format(x,y))
        self.stuck = False
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        
class seeker_AI(AI):
    '''
        This AI tries to find and kill the hero. Should be improved later
    '''
    def ACT(self, circumstances, Time):
        self.stuck = False
        h = circumstances.get_hero()
        hx, hy = h.position
        x, y = self.who.position
        if not self.who.can('see'):
            MSG.pop(self.who.name+' cannot see!')
        if self.who.can('see') and circumstances.visible_by(self.who, hx, hy):
            self.memorize(0, (hx, hy))
            self.memorize(1,(hx - x, hy - y))
            self.memorize(2, 20)
            if self.who.light == 10000:
                self.who.light = 5
                MSG.pop('You hear someone whisper: "W-h-h-e s-s-see the hobbitses-s-s..."')
                log(self.who.name+'\'s seeker AI deactivates light')
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
                log(self.who.name+'\'s seeker AI activates light')
        Time.after(self.who.get_stat('SPD'), lambda:self.act(circumstances, Time))
        l = circumstances.can_move_creature(self.who, -1, 0)
        r = circumstances.can_move_creature(self.who, 1, 0)
        u = circumstances.can_move_creature(self.who, 0, -1)
        d = circumstances.can_move_creature(self.who, 0, 1)
        dx, dy = hx - x, hy - y
        if abs(dx)>abs(dy):
            if dx > 0 and r:
                circumstances.move_creature(self.who, 1, 0)
                log(self.who.name+'\'s seeker AI decides to go right')
            elif dx < 0 and l:
                circumstances.move_creature(self.who, -1, 0)
                log(self.who.name+'\'s seeker AI decides to go left')
        else:
            if dy > 0 and d:
                circumstances.move_creature(self.who, 0, 1)
                log(self.who.name+'\'s seeker AI decides to go down')
            elif dy < 0 and u:
                circumstances.move_creature(self.who, 0, -1)
                log(self.who.name+'\'s seeker AI decides to go up')
        
        
        
        
        
        
        
        
        
        
