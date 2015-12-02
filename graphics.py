import curses

keys = {'down':258, 'up':259, 'left':260, 'right':261, 'enter': 10, 'esc': 263, 'i':105} #27 - esc

#Delay of the main menu may be caused by the ESC key delay, using backspace instead for now

def print(*args):
    log = open('log.txt', 'a')
    log.write(' '.join(str(i) for i in args) + '\n')
    log.close()
    
def reset_log():
    log = open('log.txt', 'w')
    log.close()

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

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

    color_pairs = {'normal': curses.color_pair(1), 
                   'highlight': curses.color_pair(2),
                   'red': curses.color_pair(3),
                   'attention': curses.color_pair(3),
                   'green': curses.color_pair(4),
                   'yellow': curses.color_pair(5),
                   'white': curses.color_pair(1),
                   'brown': curses.color_pair(6),
                   'blue': curses.color_pair(7)}

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
    def draw_windows():
        for window in Window.__register:
            if window != Window.focused_window and window.visible:
                window.draw()
        if Window.focused_window != None and Window.focused_window.visible:
            Window.focused_window.draw()
    def get_event(event):
        if Window.focused_window != None:
            Window.focused_window.accept_event(event)
    def accept_event(self, event):
        if self.back != None and event == keys['esc']:
            self.back()
        for element in self.ems:
            if isinstance(element, KeyAcceptorElement) and element.can_accept_event(event):
                element.accept_event(event)
        if self.focused_element != None:
            if self.focused_element.can_accept_event(event):
                self.focused_element.accept_event(event)
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
        self.visible = False
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
    def draw(self):
        for x in range(self.x, self.x+self.w):
            for y in range(self.y, self.y+self.h):
                win.addch(y,x,' ')
        if not self.noborder:
            for x in [self.x, self.x + self.w - 1]:
                for y in range(self.y, self.y+self.h):
                    win.addch(y,x,'|')
            for x in range(self.x+1, self.x+self.w-1):
                for y in [self.y, self.y + self.h - 1]:
                    win.addch(y,x,'=')
            for x in range(len(self.title)):
                if self.bold:
                    win.addch(self.y,self.x + (self.w - len(self.title))//2 + x,self.title[x], curses.A_BOLD)
                else:
                    win.addch(self.y,self.x + (self.w - len(self.title))//2 + x,self.title[x])
        for e in self.ems:
            e.draw()
    def add_element(self, element):
        assert(isinstance(element, WindowElement))
        assert(element.parent == None)
        element.parent = self
        self.ems.append(element)
        if element.can_accept_focus:
            self.focus_acceptors.append(element)
        
class WindowElement:
    parent = None
    can_accept_focus = False
    def can_accept_events(self, event):
        return False
    def __init__(self, *args):
        raise ValueError('Cannot create objects of WindowElement class')
    def draw(self):
        raise NotImplementedError('Drawing not implemented for', type(self))
    def get_focus(self):
        self.has_focus = True
    def reset(self):
        print('Warning: reset method not implemented for', type(self))
        
class TextElement(WindowElement):
    def __init__(self, x, y, text, style=''): #x, y relative to the window, starting from 1 for windows with borders
        self.bold = 'b' in style #Just an example, more are coming TODO
        self.red = 'r' in style
        self.x, self.y = x, y
        self.text = text
    def draw(self):
        if not isinstance(self.parent, Window): raise ValueError('Cannot draw a TextElement without a parent')
        for i in range(len(self.text)):
            mod = 0
            if self.bold: mod += curses.A_BOLD
            if self.red: mod += color_pairs['attention']
            win.addch(self.parent.y + self.y, self.parent.x + self.x + i, self.text[i], mod)
                
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
    def __init__(self, x, y, bindings): #Bindings is a list of tuples: [(text, command-function), ...]
        self.x, self.y = x, y
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
                    win.addch(self.parent.y + self.y + n, self.parent.x + self.x + i, self.bindings[n][0][i], color_pairs['highlight'])
                else:
                    win.addch(self.parent.y + self.y + n, self.parent.x + self.x + i, self.bindings[n][0][i])   
    
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
        print(self.text_map)
        for x in range(self.w):
            for y in range(self.h):
                win.addch(self.parent.y + self.y + y, self.parent.x + self.x + x, self.text_map[y][x], color_pairs[self.color_map[y][x]])
                
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
   
init_graphics()
               
