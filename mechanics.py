import graphics
MSG = graphics.MessageBox
ask = graphics.YesNoBox.ask
from hero import hero
from creatures import Creature
from tweaks import log as LOG
from time import sleep
from mapgen import Map

log = lambda *x: LOG(*x, f='logs/mechanics.log')

class Time:
    now = 0
    times = []
    actions = []
    ids = []
    __curr_id = 0
    def after(time, action):
        for c in Map.get_creatures():
            if c.alive and not c.check_health():
                c.die()
        if Time.times == []:
            Time.times = [time+Time.now]
            Time.actions = [action]
            Time.__curr_id += 1
            Time.ids = [Time.__curr_id]
            return Time.__curr_id
        if time + Time.now >= Time.times[-1]:
            Time.times.append(time+Time.now)
            Time.actions.append(action)
            Time.__curr_id += 1
            Time.ids.append(Time.__curr_id)
            return Time.__curr_id
        for i in range(len(Time.times)):
            if Time.times[i] > time + Time.now:
                Time.times[i:i] = [time+Time.now]
                Time.actions[i:i] = [action]
                Time.__curr_id += 1
                Time.ids[i:i] = [Time.__curr_id]
                return Time.__curr_id
    def wait(t=100):
        log(Time.times)
        for c in Map.get_creatures():
            if c.alive and not c.check_health():
                c.die()
        for i in range(t):
            Time.now += 1
            count = 0
            for k in range(len(Time.times)):
                if Time.times[k] > Time.now:
                    break
                else:
                    count += 1
                    Time.actions[k]()
            Time.times = Time.times[count:]
            Time.actions = Time.actions[count:]
            Time.ids = Time.ids[count:]
    def wait_until_next_event():
        for c in Map.get_creatures():
            if c.alive and not c.check_health():
                c.die()
        if Time.times == []: return
        Time.now = Time.times[0]
        Time.actions[0]()
        Time.times = Time.times[1:]
        Time.actions = Time.actions[1:]
        Time.ids = Time.ids[1:]
    def wait_until_event(ev_id):
        for c in Map.get_creatures():
            if c.alive and not c.check_health():
                c.die()
        if ev_id not in Time.ids: 
            log(Time.times, Time.ids, Time.actions)
            raise ValueError('No such event!')
        else:
            g = Time.ids.index(ev_id)
            t = Time.times[g]
            Time.wait(t-Time.now)
            return t
            

def player_acts(command, field):
    if field.get_hero().AI == None:
        if hero.alive:
            operate(command, field)
            next = Time.after(field.get_hero().get_stat('SPD'), lambda:operate('wait', field))
        else:
            next = Time.after(field.get_hero().get_stat('SPD'), lambda:operate('wait', field))
            MSG.pop('You are too dead')
    else:
        next = None
    if field.get_hero().AI != None:
        sleep(0.01)
        pass
    for c in field.get_creatures():
        AI = c.AI
        if AI != None and AI.stuck:
            AI.act(field, Time)
    if next:
        t=Time.wait_until_event(next)
    else:
        Time.wait(t=field.get_hero().get_stat('SPD'))
        
    
        
def operate(command, field):
    if command == 'commit suicide':
        if ask('Are you sure you want to commit suicide?'): #Perhaps it should be asked a little bit earlier
            hero.die()
    elif command == 'down':
        if not field.move_creature(hero, 0, 1):
            MSG.pop('You can\'t walk there!')
    elif command == 'up':
        if not field.move_creature(hero, 0, -1):
            MSG.pop('You can\'t walk there!')
    elif command == 'left':
        if not field.move_creature(hero, -1, 0):
            MSG.pop('You can\'t walk there!')
    elif command == 'right':
        if not field.move_creature(hero, 1, 0):
            MSG.pop('You can\'t walk there!')
    elif command == 'wait':
        passk=None
    elif command == 'open door':
        k= None
        x, y = hero.position
        while k not in [graphics.keys[i] for i in ('left', 'right', 'up', 'down')]:
            k=graphics.stdscr.getch()
        if k == graphics.keys['left']:
            for s in Map.statics:
                if (s.x, s.y) == (x-1, y):
                    hero.open_door(s)
        elif k == graphics.keys['right']:
            for s in Map.statics:
                if (s.x, s.y) == (x+1, y):
                    hero.open_door(s)
        elif k == graphics.keys['up']:
            for s in Map.statics:
                if (s.x, s.y) == (x, y-1):
                    hero.open_door(s)
        elif k == graphics.keys['down']:
            for s in Map.statics:
                if (s.x, s.y) == (x, y+1):
                    hero.open_door(s)
    elif command == 'close door':
        k= None
        x, y = hero.position
        while k not in [graphics.keys[i] for i in ('left', 'right', 'up', 'down')]:
            k=graphics.stdscr.getch()
        if k == graphics.keys['left']:
            for s in Map.statics:
                if (s.x, s.y) == (x-1, y):
                    hero.close_door(s)
        elif k == graphics.keys['right']:
            for s in Map.statics:
                if (s.x, s.y) == (x+1, y):
                    hero.close_door(s)
        elif k == graphics.keys['up']:
            for s in Map.statics:
                if (s.x, s.y) == (x, y-1):
                    hero.close_door(s)
        elif k == graphics.keys['down']:
            for s in Map.statics:
                if (s.x, s.y) == (x, y+1):
                    hero.close_door(s)
    elif command == 'attack':
        k= None
        x, y = hero.position
        while k not in [graphics.keys[i] for i in ('left', 'right', 'up', 'down')]:
            k=graphics.stdscr.getch()
        
        if k == graphics.keys['left']:
            pass
        elif k == graphics.keys['right']:
            pass
        elif k == graphics.keys['up']:
            pass
        elif k == graphics.keys['down']:
            pass
        
