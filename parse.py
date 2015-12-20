#This file is Orthodox
from tweaks import read_file
from tweaks import log as LOG

log = lambda *x: LOG(*x, f='logs/parse.log')

def read_materials():
    '''
        This function processes data from materials.txt and returns
        a list of dictionaries, each of them represents a material.
    '''
    fname = './lore/for_robots/materials.txt'
    try:
        I = open(fname, 'r')
    except:
        log('Materials file not fount, raising error')
        raise Exception('materials file not found')
    props = []
    mats = []
    mode = None
    d = None
    for l in I:
        l = l.strip()
        if l == 'properties:':
            mode = 'props'
            continue
        if l == 'materials:':
            mode = 'mat'
            continue
        if l == '': continue
        if mode == 'props':
            props.append(l)
        elif mode == 'mat':
            if l[:5] == 'name:':
                if d != None: mats.append(d)
                d = {'name': l[5:]}
                continue
            x, y = l.split(':')
            for p in props:
                if x == p:
                    d[x] = y
    log(str(len(mats)), 'materials have been parsed')
    return mats
    
def read_tiles():
    '''
        This function processes data from tiles.txt and returns
        a dictionary in which each pair represents the link between
        the tile's name and its symbol. Makes tiles.py redundant.
    '''
    ascii = {}
    text = read_file('ascii_tiles.txt').split('\n')
    for match in text:
        if match == '': continue
        ascii[match[:-2]] = match[-1]
    log(str(len(ascii)), 'tiles have been parsed')
    return ascii
    
def read_colors():
    '''
        This function processes data from colors.txt and returns a dictionary:
            {string name -> tuple(int color's number, int red 0-1000, int green 0-1000, int blue 0-1000)},
        representing one color. The color's number is used to prevent the dictionary from
        mixing the colors.
    '''
    colors = {}
    lines = read_file('./lore/for_robots/colors.txt').split('\n')
    for line in lines:
        if line == '' or '#' in line:
            continue
        num, name, R, G, B = line.split(' ')
        colors[name] = (int(num),) + tuple(int(int(CL, 16) * 1000 / 255) for CL in (R, G, B))
    log(str(len(colors)), 'colors have been parsed')
    return colors
    
def read_statics():
    '''
        This function processes data from statics.txt and returns a list of dictionaries:
            {string property -> int/bool/string/etc. value}
    '''
    statics = []
    lines = read_file('./lore/for_robots/statics.txt').split('\n')
    st = {}
    for line in lines:
        if line == '' or '#' in line:
            continue
        line = line.strip().replace(' ', '')
        if line[-1] == ':':
            if st != {}:
                statics.append(st)
            st = {'name': line[:-1].lower()}
        elif line == 'notpassible':
            st['passible'] = False
        elif line == 'passible':
            st['passible'] = True
        elif 'lightsource' in line:
            line = line.split(':')
            if '-' in line[1]:
                line[1] = line[1].split('-')
                st['light'] = range(int(line[1][0]), int(line[1][1]))
            elif ',' in line[1]:
                line[1] = line[1].split(',')
                st['light'] = tuple(int(i) for i in line[1])
            else:
                st['light'] = int(line[1])
        elif 'symbol' in line:
            st['symbol'] = line[-1]
        elif 'color' in line:
            line = line.split(':')
            if ',' in line[1]:
                line[1] = line[1].split(',')
            st['color'] = line[1]
        elif line == 'blocksvision':
            st['transparent'] = False
    if st != {}:
        statics.append(st)
    log(str(len(statics)), 'statics have been parsed')
    return statics
    
    
    
    
    
