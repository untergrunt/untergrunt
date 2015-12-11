import curses
import parse

keys = {'down':258, 'up':259, 'left':260, 'right':261, 'enter': 10, 'esc': 263, 'i':105, 'k': 11, '.': 46} #27 - esc, 263 - backspace
for i in range(97, 123):
    keys[chr(i)] = i

table_symbols = {'-': '─', '|': '│', 'ul': '┌', 'll': '└', 'ur': '┐', 'lr': '┘'}

#Delay of the main menu may be caused by the ESC key delay, using backspace instead for now

def print(*args, end='\n'):
    log = open('log.txt', 'a')
    log.write(' '.join(str(i) for i in args) + end)
    log.close()
    
def reset_log():
    log = open('log.txt', 'w')
    log.close()
    pass

def init_graphics():
    global stdscr, win, height, width, color_pairs
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    curses.curs_set(0)
    curses.start_color()

    begin_x = 0; begin_y = 0
    height = curses.LINES
    width = curses.COLS
    win = curses.newwin(height+1, width+1, begin_y, begin_x)

    cls = parse.read_colors()
    colors = [(i[0], i[1][1:]) for i in sorted(list(cls.items()), key=lambda x: x[1][0])]
    color_number = len(colors)
    print(colors)
    cls = {}
    for i in range(color_number):
        curses.init_color(16+i, *colors[i][1])
        cls[colors[i][0]]=16+i
    print(cls)
    color_pairs = {}
    for i in range(color_number):
        for j in range(color_number):
            curses.init_pair(16+i*16+j, cls[colors[i][0]], cls[colors[j][0]])
            color_pairs[colors[i][0] + '+' + colors[j][0]] = curses.color_pair(16+i*16+j)
            
init_graphics()
bgcolor = 'dark_gray'
fgcolor = 'white'

def die():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

def interact(interpreter):
    ''' 
        The function that is normally called Mainloop,
        gets user input and passes it to the interpreter function.
        Exits if interpreter returns False 
    '''
    while True:
        a=stdscr.getch()
        if interpreter(a) == False: break
        
class Window:
    focused_window = None
    __register = []
    name = None
    element_focus_stack = []
    def key_acceptor_function(self, event): 
        '''
            This function decides what to do with any event sent to its elements
            When unable to handle an event, returns False, otherwise True
            Must be overriden for specific behaviour like that:
                def foo(self, event):
                    Do something
                    return True of False
                my_window.key_acceptor_function = foo
        '''
        accepted_flag = False
        for element in self.ems:
            if isinstance(element, KeyAcceptorElement) and element.can_accept_event(event):
                element.accept_event(event) #All KeyAcceptors allways get treir events
                accepted_flag = True
        if self.focused_element != None:
            if self.focused_element.can_accept_event(event):
                self.focused_element.accept_event(event)
                accepted_flag  = True
        return accepted_flag
    def draw_windows():
        print('new')
        for window in Window.__register:
            print(window.visible, window.name)
        for window in Window.__register:
            if window != Window.focused_window and window.visible:
                window.draw()
        if Window.focused_window != None and Window.focused_window.visible:
            Window.focused_window.draw()
    def get_event(event):
        if Window.focused_window != None:
            Window.focused_window.accept_event(event)
    def accept_event(self, event):
        if not self.key_acceptor_function(event):
            if self.back != None and event == keys['esc']:
                self.back()
    def __init__(self, x, y, w, h, title = '', back=None, style=''):
        self.has_focus = False
        self.back = back
        assert(type(title) == str)
        assert(all(type(i) == int for i in [x, y, h, w]))
        assert(type(style) == str)
        self.title = title
        if title != '':
            if len(title) > w: raise ValueError('Title cannot be longer than the window')
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ems = []
        self.focus_acceptors = []
        self.focused_element = None
        self.bold = 'b' in style
        self.noborder = 'n' in style
        self.red = 'r' in style
        self.visible = False
        self.element_focus_stack = []
        Window.__register.append(self)
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False
    def wipe(self):
        self.has_focus = False
        self.ems = []
        self.focus_acceptors = []
        self.focused_element = None
    def reset(self):
        self.has_focus = False
        self.focused_element = None
        for element in self.ems:
            element.reset()
    def get_focus(self):
        if Window.focused_window != None:
            Window.focused_window.has_focus = False
        Window.focused_window = self
        self.has_focus = True
        if self.focused_element == None:
            if self.focus_acceptors != []:
                self.focus_acceptors[0].get_focus()
                self.focused_element = self.focus_acceptors[0]
        self.show()
    def lose_focus(self):
        if self.has_focus:
            self.has_focus = False
            Window.focused_window = None
            self.focused_element.lose_focus()
            self.focused_element = None
    def pass_internal_focus(self, e):
        assert(e in self.ems)
        self.element_focus_stack.append(self.focused_element) #May be VERY buggy later
        e.has_focus = True
        self.focused_element = e
    def draw(self):
        for x in range(self.x, self.x+self.w):
            for y in range(self.y, self.y+self.h):
                win.addch(y,x,' ',color_pairs[fgcolor + '+'+bgcolor])
        if not self.noborder:
            stl = color_pairs['red+'+bgcolor] if self.red else color_pairs[fgcolor + '+'+bgcolor]
            for x in [self.x, self.x + self.w - 1]:
                for y in range(self.y, self.y+self.h):
                    win.addch(y,x,table_symbols['|'], stl)
            for x in range(self.x+1, self.x+self.w-1):
                for y in [self.y, self.y + self.h - 1]:
                    win.addch(y,x,table_symbols['-'], stl)
            win.addch(self.y, self.x, table_symbols['ul'], stl)
            win.addch(self.y + self.h - 1, self.x, table_symbols['ll'], stl)
            win.addch(self.y, self.x + self.w - 1, table_symbols['ur'], stl)
            win.addch(self.y + self.h - 1, self.x + self.w - 1, table_symbols['lr'], stl)
            stl += curses.A_BOLD if self.bold else 0
            for x in range(len(self.title)):
                    win.addch(self.y,self.x + (self.w - len(self.title))//2 + x,self.title[x], stl)
        for e in self.ems:
            if  e.visible:
                e.draw()
    def add_element(self, element):
        assert(isinstance(element, WindowElement))
        assert(element.parent == None)
        element.parent = self
        self.ems.append(element)
        if element.can_accept_focus:
            self.focus_acceptors.append(element)
    def get_reg():
        return Window.__register
        
              
class MessageBox(Window):
    def __init__(self, text, back=None):
        l = len(text)
        maxlen = 80
        if l < maxlen:
            w = l + 10
            h = 5
        else:
            w = maxlen + 10
            n = l // maxlen
            h = n + 5
        self.w = max(w, 40)
        self.h = h
        kae = KeyAcceptorElement({keys['enter']: back})
        self.x = (width - self.w) // 2
        self.y = (height - self.h) // 2
        self.ems = [kae]
        self.focus_acceptors = [kae]
        self.focused_element = kae
        self.bold = False
        self.noborder = False
        self.visible = False
        self.title = 'Attention!(Press <enter> to discard)'
        self.has_focus = False
        if back != None:
            self.back = back
        self.red = True
        kae.parent = self
        if l < maxlen and '\n' not in text:
            txt = LabelElement(5,2,text)
        else:
            self.h += text.count('\n')
            txt = TextElement(5,2,maxlen,text)
        self.add_element(txt)
    def pop(msg, prev_window=None):
        if prev_window == None:
            prev_window = MessageBox.back
        A = MessageBox(msg, lambda: prev_window.get_focus())
        A.get_focus()
        
class WindowElement:
    parent = None
    can_accept_focus = False
    visible = True
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False
    def can_accept_events(self, event):
        return False
    def __init__(self, *args):
        raise ValueError('Cannot create objects of WindowElement class')
    def draw(self):
        raise NotImplementedError('Drawing not implemented for', type(self))
    def get_focus(self):
        self.has_focus = True
        self.parent.pass_internal_focus(self)
    def reset(self):
        print('Warning: reset method not implemented for', type(self))
        
class LabelElement(WindowElement):
    def __init__(self, x, y, text, style=''): #x, y relative to the window, starting from 1 for windows with borders
        self.bold = 'b' in style #Just an example, more are coming TODO
        self.red = 'r' in style
        self.x, self.y = x, y
        self.text = text
    def draw(self):
        if not isinstance(self.parent, Window): raise ValueError('Cannot draw a LabelElement without a parent')
        for i in range(len(self.text)):
            mod = 0
            if self.bold: mod += curses.A_BOLD
            if self.red: mod += color_pairs['red+'+bgcolor]
            else:
                mod += color_pairs[fgcolor + '+'+bgcolor]
            win.addch(self.parent.y + self.y, self.parent.x + self.x + i, self.text[i], mod)
            
class TextElement(WindowElement):
    def __init__(self, x, y, w, text, style=''): #x, y relative to the window, should start from 1 for windows with borders
        self.bold = 'b' in style #Just an example, more are coming TODO
        self.red = 'r' in style
        self.x, self.y = x, y
        self.text = text
        self.w = w
    def draw(self):
        if not isinstance(self.parent, Window): raise ValueError('Cannot draw a TextElement without a parent')
        mod = 0
        if self.bold: mod += curses.A_BOLD
        if self.red: mod += color_pairs['red+'+bgcolor]
        else: mod += color_pairs[fgcolor + '+'+bgcolor]
        parts = self.text.split('\n')
        for z in range(len(parts)):
            part = parts[z]
            l = len(part)
            w = self.w
            h = l // w
            #Draw the natural part of the text
            for y in range(h):
               for x in range(w):
                   win.addch(self.parent.y + self.y + y + z, self.parent.x + self.x + x, part[y*w+x], mod)
            #Draw the rest
            for i in range(l - w * h):
               win.addch(self.parent.y + self.y + h + z, self.parent.x + self.x + i, part[w*h + i], mod)
                
class VerticalMenuElement(WindowElement):
    def can_accept_event(self, event):
        dulr = [258, 259, 260, 261, 10]
        return event in dulr
    def accept_event(self, event):
        if event == keys['down']:
            self.scroll_focus_down()
        elif  event == keys['up']:
            self.scroll_focus_up()
        elif event == keys['left']:
            pass
        elif event == keys['right']:
            if self.focused_element != None:
                self.bindings[self.focused_element][1]()
        elif event == keys['enter']:
            if self.focused_element != None:
                self.bindings[self.focused_element][1]()
    def __init__(self, x, y, bindings, cls=
        {
            'normal': color_pairs[fgcolor + '+'+bgcolor],
            'selected': color_pairs[bgcolor+'+white'],
        }): #Bindings is a list of tuples: [(text, command-function), ...]
        self.x, self.y = x, y
        self.cls = cls
        print('===', cls)
        self.bindings = bindings
        assert(all('\n' not in i for i in bindings))
        self.can_accept_focus = True
        self.focused_element = None
        self.has_focus = False
    def reset(self):
        self.focused_element = None
        self.has_focus = False
    def get_focus(self):
        if self.focused_element == None:
            self.focused_element = 0
        self.has_focus = True
        self.parent.pass_internal_focus(self)
    def scroll_focus_down(self):
        assert(self.focused_element == None or self.focused_element in range(len(self.bindings)))
        if self.focused_element in [None, len(self.bindings) - 1]:
            self.focused_element = 0
        else:
            self.focused_element += 1
    def scroll_focus_up(self):
        assert(self.focused_element == None or self.focused_element in range(len(self.bindings)))
        if self.focused_element in [None, 0]:
            self.focused_element = len(self.bindings) - 1
        else:
            self.focused_element -= 1
    def lose_focus(self):
        self.focused_element = 0
        self.has_focus = False
    def draw(self):
        for n in range(len(self.bindings)):
            for i in range(len(self.bindings[n][0])):
                if self.focused_element == n:
                    stl = self.cls['selected']
                    win.addch(self.parent.y + self.y + n, self.parent.x + self.x + i, self.bindings[n][0][i], stl)
                else:
                    stl = self.cls['normal']
                    win.addch(self.parent.y + self.y + n, self.parent.x + self.x + i, self.bindings[n][0][i], stl)   
    
class DfViewElement(WindowElement):
    def can_accept_event(self, event):
        if 'accepts_keys' in dir(self) and event in self.accepts_keys: return True
        return False
    def accept_event(self, event):
        self.actions[event]()
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text_map = None
        self.color_map = None    
    def set_text_map(self, text_map):
        if type(text_map) == str:
            self.text_map = [[text_map for x in range(self.w)]for y in range(self.h)]
        else:
            assert(len(text_map) == self.w)
            assert(all(len(i) == self.h for i in text_map))
            self.text_map = text_map
    def set_color_map(self, color_map):
        if type(color_map) == str:
            self.color_map = [[color_map for x in range(self.w)]for y in range(self.h)]
        else:
            assert(len(color_map) == self.w)
            assert(all(len(i) == self.h for i in color_map))
            self.color_map = color_map
    def draw(self):
        if self.text_map == None: return
        #print(self.text_map)
        for x in range(self.w):
            for y in range(self.h):
                win.addch(self.parent.y + self.y + y, self.parent.x + self.x + x, self.text_map[y][x], color_pairs[self.color_map[y][x]+'+'+bgcolor])
                
class KeyAcceptorElement(WindowElement):
    def __init__(self, dic):
        assert(type(dic) == dict)
        assert(all(type(x) == int for x in dic.keys()))
        self.dic = dic
    def can_accept_event(self, event):
        return event in self.dic
    def draw(self):
        pass
    def accept_event(self, event):
        self.dic[event]()
        
class CursorElement(WindowElement):
    def __init__(self, min_x, min_y, max_x, max_y, enter_handler):
        assert(all(type(i) == int for i in [min_x, min_y, max_x, max_y]))
        self.min_x, self.min_y, self.max_x, self.max_y = min_x, min_y, max_x, max_y
        self.x = (min_x + max_x) // 2
        self.y = (min_y + max_y) // 2
        self.handler = enter_handler
        self.visible = False
    def can_accept_event(self, event):
        return event in [keys['down'], keys['up'], keys['left'], keys['right'], keys['enter'], keys['esc']]
    def draw(self):
        win.addch(self.parent.y + self. y, self.parent.x + self.x, 'X', color_pairs['red+'+bgcolor])
    def accept_event(self, event):
        if event == keys['down']:
            if self.y < self.max_y:
                self.y += 1
        elif event == keys['up']:
            if self.y > self.min_y:
                self.y -= 1
        elif event == keys['right']:
            if self.x < self.max_x:
                self.x += 1
        elif event == keys['left']:
            if self.x > self.min_x:
                self.x -= 1   
        elif event == keys['esc']:
            self.has_focus = False
            self.parent.focused_element = self.parent.element_focus_stack.pop()
            self.hide()
        else:
            self.handler(self, self.x, self.y)
    def handler(self, x, y):
        pass
    def get_focus(self):
        self.x = (self.min_x + self.max_x) // 2
        self.y = (self.min_y + self.max_y) // 2        
        self.has_focus = True
        self.parent.pass_internal_focus(self)
        self.visible = True
            
            
            
init_graphics()
               
