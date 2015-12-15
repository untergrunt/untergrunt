from creatures import *
        
hero = Creature(human_race, 'Urist', bdy)
hero.symbol = '@'
hero.AI = None#random_AI(hero)
hero.stats.dic['SPD'] = 9
hero.controlled_by_player = True

gob = Creature(goblin_race, 'Kek', bdy)
gob.light = 100

hero.light = 100

gob.AI = seeker_AI(gob)
