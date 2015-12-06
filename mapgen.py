from field import *
from graphics import print
from os import mkdir, listdir

class BigMap:
    '''
        The class keeps __all__ the data about current 'level'; that includes:
            -- Every cell's floor and fill materials (done)
            -- Every creature on the map
            -- Every static object (decorations, e.g. stones and trees)
            -- Everything on the floor (e.g. dropped weapons and small stones)
    '''
    def __init__(self, alg, w, h):
        '''
            w stands for width in tiles,
            h for height in tiles,
            alg for the type of generation algorythm
        '''
        assert(alg in ['dungeon', 'village', 'lenoblast', 'plane'])
        self.alg = alg
        self.w = w
        self.h = h
        self.__ready = False
        self.__creatures = {}
    def generate(self):
        generators = {
            'dungeon': BigMap.generate_dungeon,
            'village': BigMap.generate_village,
            'lenoblast': BigMap.generate_lenoblast,
            'plane': BigMap.generate_plane
        }
        self.m = generators[self.alg](self.w, self.h)
        self.__ready = True
    def ready(self):
        return self.__ready
    def generate_dungeon(w, h):
        bm = [[Cell('stone','stone')] * w for i in range(h)]
        for y in range(450,550):
            for x in range(450,550):
                bm[y][x] = Cell('stone','air')
        return bm
    def generate_village(w, h): #TODO
        pass
    def generate_lenoblast(w, h): #TODO
        pass
    def generate_plane(w, h):
        m = [[Cell('stone','air') for i in range(w)] for j in range(h)]
        return m
    def save(self, fname='world'):
        files = listdir('save')
        assert(self.ready())
        def save_to_dir(dirname):
            mkdir(dirname)
            #FIXME
            '''
            for y in range(len(self.chunks)):
                for x in range(len(self.chunks[y])):
                    O = open('{}/chunk_{}_{}.save'.format(dirname, x, y), 'w')
                    O.write(str(self.chunks[x][y]))
                    O.close()
            '''
        if fname not in files:
            save_to_dir('save/'+fname)
        else:
            n=1
            while fname + str(n) in files:
                n += 1
            save_to_dir('save/'+fname+str(n))
    def add_creature(self, creature, x, y):
        if creature.id not in self.__creatures:
            self.__creatures[creature.id] = (x, y)
    def where_is(self, creature):
        try:
            return self.__creatures[creature.id]
        except:
            raise ValueError('Could not find such a creature')
    def knows(self, creature):
        return creature.id in self.__creatures
    def move_creature(self, creature, x, y):
        try:
            x0, y0 = self.__creatures[creature.id]
            if creature.can_pass_through(self.m[y0 + y][x0 + x]):
                self.__creatures[creature.id] = (x0 + x, y0 + y)
                return True
            else:
                return False
        except:
            raise ValueError('Could not find such a creature')
            
            
            
    
    
    
