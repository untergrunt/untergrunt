import windows
from windows import graphics
import tweaks

log = lambda *x: tweaks.log(*x, f='main.log')

tweaks.reset_logs()

graphics.init_graphics()
windows.load_main_window()
graphics.Window.draw_windows()
graphics.win.refresh()

keys = graphics.keys

def event_manager(event):
    if event == 113:
        return False
    else:
        graphics.Window.get_event(event)
        graphics.Window.draw_windows()
        graphics.win.refresh()
#        print(event)
    

graphics.interact(event_manager)

graphics.die()
