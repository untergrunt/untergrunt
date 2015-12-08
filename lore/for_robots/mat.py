def is_blank(s):
    return set(s) in set('\n\t ')#FIXME

act = ''

def ask_yn(question):
    yes = ['yes', 'y', 'sure', 'ok', 'of course']
    no = ['no', 'nope', 'n', 'not now']
    a = input(question + '\n').strip()
    while a not in yes + no:
        print('Could not understand you :(')
        a = input(question + '\n').strip()
    return a in yes

end_commands = ['exit', 'quit', 'q', 'stop']
creation_commands = ['create', 'new', 'add']
commands = end_commands + creation_commands

def create_material():
    props = []

    I = open('materials.txt', 'r')
    for line in I:
        if 'properties' in line: continue
        if line.strip() == 'materials:': break
        else:
            props.append(line.strip())
    I.close()
    F = open('materials.txt', 'a')
    r = []
    nm = input('\nWhat will be the name?\n') 
    if nm == 'stop':
        F.close()
        return False
    for p in props:
        r.append(input('What will be the ' + p + '?\n'))
    F.write('\nname:'+nm)
    for p in range(len(r)):
        F.write('\n\t'+props[p]+':'+r[p])
    F.close()
    return True

while act not in end_commands:
    act = input('\nWhat do you want to do?\n').strip()
    while act not in commands:
        act = input('Cannot understand you, try again please:\n').strip()
    if act in creation_commands:
        inf = ask_yn('Do you want to create multiple materials?')
        if not inf:
            create_material()
        else:
            while create_material():
                pass


