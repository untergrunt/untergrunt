from field import *
from graphics import print
from os import mkdir, listdir
from creatures import Creature

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
        self.ambient_light = 30
        self.lightmap = [[self.ambient_light]*w for i in range(h)]
        self.sources = None
        self.statics = []
    def generate(self):
        generators = {
            'dungeon': BigMap.generate_dungeon,
            'village': BigMap.generate_village,
            'lenoblast': BigMap.generate_lenoblast,
            'plane': BigMap.generate_plane
        }
        mp = generators[self.alg](self.w, self.h)
        self.m = mp[0]
        self.statics = mp[1]
        self.__ready = True
    def ready(self):
        return self.__ready
    def generate_dungeon(w, h):
        bm = [[Cell('stone','air') for j in range(w)] for i in range(h)]
        for i in range(1,25):
                for k in range(w):
                    bm[(h-1)//25 * i][k] = Cell('stone','stone')
                    bm[k][(w-1)//25 * i] = Cell('stone','stone')
        for i in range(1,25):
                for k in range(100,w-100):
                    bm[(h-1)//25 * i + 5][k] = Cell('stone','air')
                    bm[k][(w-1)//25 * i + 5] = Cell('stone','air')
        stats = [Static('door', i[0], i[1]) for i in [(507, 473), (468,473), (473, 468), (473, 507)]]
        for s in stats:
            if bm[s.y][s.x].statics == None:
                bm[s.y][s.x].statics = [s]
            else:
                bm[s.y][s.x].statics.append(s)
        return [bm, stats]
    def generate_village(w, h): #TODO
        pass
    def generate_lenoblast(w, h): #TODO
        pass
    def generate_plane(w, h):
        m = [[Cell('dirt','air') for i in range(w)] for j in range(h)]
        for x in range((w-20)//2,(w+20)//2):
            m[(h-20)//2][x] = Cell('stone','stone')
            m[(h+20)//2][x] = Cell('stone','stone')
        for y in range((h-20)//2,(h+22)//2):
            m[y][(w-20)//2] = Cell('stone','iron')
            m[y][(w+20)//2] = Cell('stone','stone')
        m[(w-20)//2][h//2] = Cell('stone','air')
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
            raise ValueError('Could not find such a creature -', creature.id)
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
    def can_move_creature(self, creature, x, y):
        try:
            x0, y0 = self.__creatures[creature.id]
            if creature.can_pass_through(self.m[y0 + y][x0 + x]):
                return True
            else:
                return False
        except:
            raise ValueError('Could not find such a creature')
    def get_creatures(self):
        return self.__creatures
    def get_hero(self):
        for c in self.__creatures:
            if Creature.by_id(c).controlled_by_player:
                return Creature.by_id(c)
        raise Exception('No hero found')
    def fov(self, c):
        x0, y0 = self.where_is(c)
        d_max = c.vision
        f = [[None]*(d_max*2) for i in range(2*d_max)]
        for i in range(2*d_max):
            xl = i
            yl = 0
            #xg = xl + x0 - d_max
            #yg = yl + x0 - d_max
    def calculate_light(self):
        creatures = [Creature.by_id(c) for c in self.__creatures]
        sources = set((self.where_is(c), c.light) for c in creatures if c.light > 0)
        statlight = set(i for i in self.statics if i.light not in [None, 0])
        if sources != self.sources:
            self.lightmap = [[self.ambient_light]*self.w for i in range(self.h)]
            for s in statlight:
                d = int((s.light - 1)**0.5)
                for lx in range(max(0,s.x-d), min(self.w,s.x+d+1)):
                    for ly in range(max(0,s.y-d), min(self.h,s.y+d+1)):
                        self.lightmap[ly][lx] += int(s.light / (((s.x-lx)**2+(s.y-ly)**2)+1))
            for c in creatures:
                z = c
                if z:
                    zx, zy = self.where_is(z)
                    if z.light > 0:
                        d = int((z.light - 1)**0.5)
                        for lx in range(max(0,zx-d), min(self.w,zx+d+1)):
                            for ly in range(max(0,zy-d), min(self.h,zy+d+1)):
                                self.lightmap[ly][lx] += int(z.light / (((zx-lx)**2+(zy-ly)**2)+1))
        self.sources = sources
                
                    
    def visible_by(self, c, x, y):
            x0, y0 = self.where_is(c)
            lt = self.lightmap[y][x]
            d_max = min(c.vision, round(c.vision * (lt/100) ** 0.5))
            if (x-x0)**2 + (y-y0)**2 > d_max**2:
                return False
            if x == x0:
                vis = True
                y1, y2 = sorted((y, y0))
                for k in range(y1+1,y2):
                    vis &= self.m[k][x].fill.name == 'air' and (self.m[k][x].statics == None or all(i.transparent for i in self.m[k][x].statics))
                return vis
            elif y == y0:
                vis = True
                x1, x2 = sorted((x, x0))
                for k in range(x1+1,x2):
                    vis &= self.m[y][k].fill.name == 'air' and (self.m[y][k].statics == None or all(i.transparent for i in self.m[y][k].statics))
                return vis
            dy = abs(y0 - y)
            dx = abs(x0 - x)
            vis1 = True
            vis2 = True
            vis3 = True
            if dy < dx:
                x1, x2 = sorted((x0, x))
                y1, y2 = sorted((y, y0))
                for i in range(x1 + 1, x2 ):
                    yy = y1 + round((y2-y1)*(x2-i)/(x2-x1))
                    vis1 &= self.m[yy][i].fill.name == 'air' and (self.m[yy][i].statics == None or all(i.transparent for i in self.m[yy][i].statics))
                    vis2 &= self.m[yy+1][i].fill.name == 'air' and (self.m[yy+1][i].statics == None or all(i.transparent for i in self.m[yy+1][i].statics))
                    vis3 &= self.m[yy-1][i].fill.name == 'air' and (self.m[yy-1][i].statics == None or all(i.transparent for i in self.m[yy-1][i].statics))
            else:
                x1, x2 = sorted((x0, x))
                y1, y2 = sorted((y, y0))
                for i in range(y1 + 1, y2 ):
                    xx = x1 + round((x2-x1)*(y2-i)/(y2-y1))
                    vis1 &= self.m[i][xx].fill.name == 'air' and (self.m[i][xx].statics == None or all(i.transparent for i in self.m[i][xx].statics))
                    vis2 &= self.m[i][xx + 1].fill.name == 'air' and (self.m[i][xx + 1].statics == None or all(i.transparent for i in self.m[i][xx + 1].statics))
                    vis3 &= self.m[i][xx - 1].fill.name == 'air' and (self.m[i][xx-1].statics == None or all(i.transparent for i in self.m[i][xx -1].statics))
            return vis1 and (vis2 or vis3)
    def add_static(self, static, x, y):
        static.x = x
        static.y = y
        self.statics.append(static)
    '''def visible_by(self, c, x, y):
            x_s, y_s = x, y
            x0, y0 = self.where_is(c)
            x0, x = sorted((x0, x)) #x0 <= x
            y0, y = sorted((y0, y)) #y0 <= y
            d_max = round(c.vision * (self.m[y][x].light/100) ** 0.5)
            if (x-x0)**2 + (y-y0)**2 > d_max**2:
                return False
            if x == x0:
                vis = True
                y1, y2 = sorted((y, y0))
                for k in range(y1+1,y2):
                    vis &= self.m[k][x].fill.name == 'air'
                return vis
            elif y == y0:
                vis = True
                x1, x2 = sorted((x, x0))
                for k in range(x1+1,x2):
                    vis &= self.m[y][k].fill.name == 'air'
                return vis
            x1, y1 = x0 + 0.5, y0 + 0.5 #x1 <= x2
            x2, y2 = x + 0.5, y + 0.5   #y1 <= y2
            for xx in range(x0 + 1, x):
                yy = int(y1 + (xx - x1)*(y2 - y1)/(x2 - x1))
                if self.m[yy][xx-1].fill.name != 'air':
                    if xx != x0 + 1 and xx != x - 1:
                        return False
                if self.m[yy][xx].fill.name != 'air':
                    return False
            for yy in range(y0 + 1, y):
                xx = int(x1 + (yy - y1)*(x2 - x1)/(y2 - y1))
                if self.m[yy-1][xx].fill.name != 'air':
                    if yy != y0 + 1 and yy != y - 1:
                        return False
                if self.m[yy][xx].fill.name != 'air':
                    return False
            return True'''
            
            
            
            
    
    
    
