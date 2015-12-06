from graphics import MessageBox as MSG
from field import hero
from creatures import Creature
#from ai import AI

def player_acts(command, field):
    operate(command, field)
    for creature in field.get_creatures():
        AI = Creature.by_id(creature).AI
        if AI != None:
            AI.act(field)
            
    
        
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
