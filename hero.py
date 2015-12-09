from creatures import *
        
hero = Creature(human_race, 'Urist')
hero.symbol = '@'
hero.AI = None#idiot_AI(hero)
hero.stats.dic['SPD'] = 10
hero.controlled_by_player = True

gob = Creature(goblin_race, 'Atol')
gob.light = 40
