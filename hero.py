from creatures import *
        
hero = Creature(human_race, 'Urist')
hero.symbol = '@'
hero.AI = None#random_AI(hero)
hero.stats.dic['SPD'] = 8
hero.controlled_by_player = True

gob = Creature(goblin_race, 'Atol')
gob.light = 0
