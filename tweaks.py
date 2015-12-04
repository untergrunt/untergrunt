def read_file(fname):
    I = open(fname, 'r')
    text = I.read()
    I.close()
    return text
    

