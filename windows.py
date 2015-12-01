import graphics
import worldgen

print = graphics.print

current_stage = 'main window'

keys = graphics.keys

def change_stage(new_stage):
    global current_stage
    if current_stage in stage_unloaders:
        stage_unloaders[current_stage]()
    assert(new_stage in stage_loaders)
    stage_loaders[new_stage]()
    current_stage = new_stage

main_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Main menu', style='n')
game_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Game window', style='n', back=lambda:change_stage('main window'))
credit_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Credits', back=lambda:change_stage('main window'), style='n')
world_creation_window = graphics.Window(0, 0, graphics.width, graphics.height, title='', back=lambda:change_stage('main window'), style='n')

def load_main_window():
    main_window.wipe()
    title_text = graphics.TextElement(graphics.width//2-7, 5,'THE ROGUELIKE!','b')
    buttons = [
    ('New game', lambda: change_stage('game')),
    ('Create new world', lambda: change_stage('new world')),
    ('Load game', lambda: print('New game loaded')),
    ('Show credits', lambda: change_stage('credits')),
    ('Quit', graphics.die)
    ]
    vmenu = graphics.VerticalMenuElement(graphics.width//3, 10, buttons)
    main_window.add_element(title_text)
    main_window.add_element(vmenu)
    main_window.get_focus()

def load_credit_window():
    credit_window.wipe()
    t1, t2, t3 = graphics.TextElement(10,10,'Credit1'), graphics.TextElement(10,11,'Credit2'), graphics.TextElement(10,12,'Credit3')
    credit_window.add_element(t1)
    credit_window.add_element(t2)
    credit_window.add_element(t3)
    credit_window.get_focus()
    
def load_world_creation_window():
    worldgen.generate()
    worldgen.export()
    map=worldgen.load_map(charnum=32)
    world_creation_window.wipe()
    dfview = graphics.DfViewElement(0,0,32,32)
    dfview.set_text_map(worldgen.map_to_strings(map))
    dfview.set_color_map(worldgen.map_to_colors(map))
    world_creation_window.add_element(dfview)
    world_creation_window.get_focus()
    world_creation_window.draw()
    
def load_game_window():
    game_window.wipe()
    dfview = graphics.DfViewElement(0,0,graphics.width,graphics.height)
    dfview.set_text_map('.')
    dfview.set_color_map('normal')
    dfview.accepts_keys = [keys['down'], keys['up'], keys['left'], keys['right']]
    dfview.actions = {keys['down']: move_character_down,
                      keys['up']: move_character_up,
                      keys['left']: move_character_left,
                      keys['right']: move_character_right}
    dfview.can_accept_focus = True
    game_window.add_element(dfview)
    game_window.get_focus()
    game_window.draw()
    
   
#FIXME The block below must be replaced with actual code, of course
    
charx, chary = 10,10    
    
def move_character_right():
    global charx
    charx+=1
    game_window.ems[0].text_map[chary][charx] = '@'
    game_window.ems[0].text_map[chary][charx-1] = '.'
def move_character_left():
    global charx
    charx-=1
    game_window.ems[0].text_map[chary][charx] = '@'
    game_window.ems[0].text_map[chary][charx+1] = '.'
def move_character_up():
    global chary
    chary-=1
    game_window.ems[0].text_map[chary][charx] = '@'
    game_window.ems[0].text_map[chary+1][charx] = '.'
def move_character_down():
    global chary
    chary+=1
    game_window.ems[0].text_map[chary][charx] = '@'
    game_window.ems[0].text_map[chary-1][charx] = '.'
    
    
    
    
    
    
    
    
    
    
    
    

stage_loaders = {'main window': load_main_window, 
                 'credits': load_credit_window, 
                 'new world': load_world_creation_window,
                 'game': load_game_window}
stage_unloaders = {}
