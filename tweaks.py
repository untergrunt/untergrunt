logging = True

def read_file(fname):
    I = open(fname, 'r')
    text = I.read()
    I.close()
    return text
    
def log(*args, f='log.txt'):
    if logging:
        logfile = open(f, 'a')
        logfile.write(' '.join(str(i) for i in args) + '\n')
        logfile.close()
