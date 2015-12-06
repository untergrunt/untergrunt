from graphics import MessageBox as MSG
from field import hero
from creatures import Creature
from tweaks import log
#from ai import AI

class Time:
    now = 0
    times = []
    actions = []
    ids = []
    __curr_id = 0
    def after(time, action):
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
        if Time.times == []: return
        Time.now = Time.times[0]
        Time.actions[0]()
        Time.times = Time.times[1:]
        Time.actions = Time.actions[1:]
        Time.ids = Time.ids[1:]
    def wait_until_event(ev_id):
        if ev_id not in Time.ids: 
            log(Time.times, Time.ids, Time.actions)
            raise ValueError('No such event!')
        else:
            g = Time.ids.index(ev_id)
            t = Time.times[g]
            Time.wait(t-Time.now)
            return t
            

def player_acts(command, field):
    next = Time.after(Creature.by_id(1).get_stat('SPD'), lambda:operate(command, field))
    for creature in field.get_creatures():
        c = Creature.by_id(creature)
        AI = c.AI
        if AI != None and AI.stuck:
            AI.act(field, Time)
    t=Time.wait_until_event(next)
            
    
        
def operate(command, field):
    if command == 'down':
        if not field.move_creature(field.hero, 0, 1):
            MSG.pop('You can\'t walk into walls!')
    elif command == 'up':
        if not field.move_creature(field.hero, 0, -1):
            MSG.pop('You can\'t walk into walls!')
    elif command == 'left':
        if not field.move_creature(field.hero, -1, 0):
            MSG.pop('You can\'t walk into walls!')
    elif command == 'right':
        if not field.move_creature(field.hero, 1, 0):
            MSG.pop('You can\'t walk into walls!')
