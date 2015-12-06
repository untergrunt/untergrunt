from graphics import MessageBox
from field import hero

def player_acts(command, field):
    if command == 'down':
        field.move_creature(field.hero, 0, 1)
    elif command == 'up':
        field.move_creature(field.hero, 0, -1)
    elif command == 'left':
        field.move_creature(field.hero, -1, 0)
    elif command == 'right':
        field.move_creature(field.hero, 1, 0)
        
        
