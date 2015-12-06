def read_file(fname):
    I = open(fname, 'r')
    text = I.read()
    I.close()
    return text
    
def log(*args):
    log = open('log.txt', 'a')
    log.write(' '.join(str(i) for i in args) + '\n')
    log.close()
