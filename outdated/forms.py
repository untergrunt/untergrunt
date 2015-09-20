import curses as c
import time as t
win = c.initscr()
c.cbreak()
#win.keypad(1)

def wait():
  a=win.getch()
  if a==ord('x'): 
    c.endwin()
    exit()
  else:
    win.refresh()
  for x in range(8):
    win.addch(4,x,c.ACS_HLINE)
    win.addch(4,8,c.ACS_PLUS)
    win.addch(4,9,c.ACS_LRCORNER)

try:
# Run your code here
    win.keypad(1)
    c.cbreak()
    scr=win.subwin(1,4,16,10)
    for x in range(1,40):
      for y in range(1,160):
        win.addch(x,y,'#')
    win.refresh()
    for x in range(20,31):
      for y in range(20,31):
        win.addch(x,y,'i')
    for i in range(len('Hello, Wolrd!')): win.addch(50+i,10,'Hello, World!'[i])
    win.addch(1,161,'E')
    win.refresh()
    while True: wait()
      #print(win.getmaxyx())
finally:
    c.nocbreak()
    win.keypad(0)
    c.echo()
    c.endwin()