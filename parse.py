from tweaks import read_file

def read_materials():
    fname = './lore/for_robots/materials.txt'
    I = open(fname, 'r')
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
    return mats
    
def read_tiles():
    ascii = {}
    text = read_file('ascii_tiles.txt').split('\n')
    for match in text:
        if match == '': continue
        assert(match.split() == [match[:-2], match[-1]])
        ascii[match[:-2]] = match[-1]
    return ascii
    
def read_colors():
    colors = {}
    lines = read_file('./lore/for_robots/colors.txt').split('\n')
    for line in lines:
        if line == '' or '#' in line:
            continue
        num, name, R, G, B = line.split(' ')
        colors[name] = (int(num),) + tuple(int(int(CL, 16) * 1000 / 255) for CL in (R, G, B))
    return colors
    
def read_statics():
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
    return statics
    
    
    
    
    
