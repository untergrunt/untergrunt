
ascii = {}

def load_tiles():
    from tweaks import read_file
    global ascii
    text = read_file('ascii_tiles.txt').split('\n')
    for match in text:
        if match == '': continue
        assert(match.split() == [match[:-2], match[-1]])
        ascii[match[:-2]] = match[-1]
    
load_tiles()
