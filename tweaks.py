def read_file(fname):
    I = open(fname, 'r')
    text = I.read()
    I.close()
    return text
    
def log(*args, f='log.txt'):
    log = open(f, 'a')
    log.write(' '.join(str(i) for i in args) + '\n')
    log.close()
