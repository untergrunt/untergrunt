def read_materials(fname):
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
    from tweaks import read_file
    ascii = {}
    text = read_file('ascii_tiles.txt').split('\n')
    for match in text:
        if match == '': continue
        assert(match.split() == [match[:-2], match[-1]])
        ascii[match[:-2]] = match[-1]
    return ascii
