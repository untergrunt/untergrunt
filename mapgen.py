from field import *
from graphics import print

class Chunk: #NEVER generates map information, only stores. Chunks are always square
    def __init__(self, size):
        self.mas = [[None] * size for i in range(size)]
        self.size = size
    def set_data(self, data):
        assert(len(self.mas) == len(data))
        self.mas = data #May cause problems later, but probably faster
    def nine_chunks_to_map(chunks): #chunks are passed as a 3x3 list
        size = chunks[0][0].size
        assert(all(all(j.size == size for j in i) for i in chunks))
        layers = sum([[sum([chunks[n][i].mas[j] for i in range(3)], []) for j in range(size)] for n in range(3)], [])
        return layers

class BigMap:
    '''
        The class keeps __all__ the data about current 'level'; that includes:
            -- Every cell's floor and fill materials
            -- Every creature on the map
            -- Every static object (decorations, e.g. stones and trees)
            -- Everything on the floor (e.g. dropped weapons and small stones)
    '''
    def __init__(self, alg, w, h, sz=256):
        '''
            w stands for width in chunks,
            h for height in chunks,
            sz for chunksize in tiles,
            alg for the type of generation algorythm
        '''
        assert(alg in ['dungeon', 'village', 'lenoblast', 'plane'])
        self.alg = alg
        self.w = w
        self.h = h
        self.sz = sz
    def generate(self):
        solution = {
            'dungeon': BigMap.generate_dungeon,
            'village': BigMap.generate_village,
            'lenoblast': BigMap.generate_lenoblast,
            'plane': BigMap.generate_plane
        }
        self.chunks = solution[self.alg](self.w, self.h, self.sz)
    def generate_dungeon(w, h, sz): #TODO
        pass
    def generate_village(w, h, sz): #TODO
        pass
    def generate_lenoblast(w, h, sz): #TODO
        pass
    def generate_plane(w, h, sz):
        m = [[Chunk(sz) for i in range(w)] for j in range(h)]
        #proc = 0 #For debugging
        for y in range(h):
            for x in range(w):
                #if (y*w+x)/(h*w) * 100 > proc:
                #    proc = int((y*w+x)/(h*w) * 100)
                #    print(proc, '%')
                m[y][x].set_data([[Cell('water', 'air') for i in range(sz)] for j in range(sz)])
        return m
    def update_needed(self, x_int, y_int, x_chunk_curr, y_chunk_curr):
        '''
            The funtion gets 4 parameters:
                -- x_int, y_int - coordinates of interest, in tiles. Normally coordinates of the hero
                -- x_chunk_curr, y_chunk_curr - upper left corner of what the camera currently has, in chunks
            The function determines whether the camera should request new chunks
        '''
        return x_int not in range(x_chunk_curr*self.sz, (x_chunk_curr + 1)*self.sz)\
            or y_int not in range(y_chunk_curr*self.sz, (y_chunk_curr + 1)*self.sz)
    def get_update(self, x_int, y_int):
        assert(x_int // self.sz + 2 < self.w)
        assert(y_int // self.sz + 2 < self.h)
        x, y = x_int // self.sz, y_int // self.sz
        return [
                Chunk.nine_chunks_to_map([i[x-1:x+3] for i in self.chunks[y-1:y+3]]),
                x,
                y
                ]
    
    
    
