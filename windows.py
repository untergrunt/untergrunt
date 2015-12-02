import graphics
import worldgen
import field

print = graphics.print

current_stage = 'main window'

keys = graphics.keys

def change_stage(new_stage):
    global current_stage
#    if new_stage == 'main window': raise Exception()
    if current_stage in stage_unloaders:
        stage_unloaders[current_stage]()
    assert(new_stage in stage_loaders)
    stage_loaders[new_stage]()
    current_stage = new_stage

main_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Main menu', style='n')
game_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Game window', style='n', back=lambda:change_stage('main window'))
credit_window = graphics.Window(0, 0, graphics.width, graphics.height, title='Credits', back=lambda:change_stage('main window'), style='n')
world_creation_window = graphics.Window(0, 0, graphics.width, graphics.height, title='', back=lambda:change_stage('main window'), style='n')

def create_main_window():
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

def load_main_window():
    main_window.reset()
    main_window.get_focus()
    

def create_credit_window():
    credit_window.wipe()
    t1, t2, t3 = graphics.TextElement(10,10,'Credit1'), graphics.TextElement(10,11,'Credit2'), graphics.TextElement(10,12,'Credit3')
    credit_window.add_element(t1)
    credit_window.add_element(t2)
    credit_window.add_element(t3)
    
def load_credit_window():
    credit_window.reset()
    credit_window.get_focus()
    
def create_world_creation_window():
    world_creation_window.wipe()
    dfview = graphics.DfViewElement(0,0,32,32)
    world_creation_window.add_element(dfview)
    
def load_world_creation_window():
    world_creation_window.reset()
    worldgen.generate()
    worldgen.export()
    map=worldgen.load_map(charnum=32)
    world_creation_window.ems[0].set_text_map(worldgen.map_to_strings(map))
    world_creation_window.ems[0].set_color_map(worldgen.map_to_colors(map))
    world_creation_window.get_focus()
    
def create_game_window():
    game_window.wipe()
    global dfview
    dfview.set_text_map('.')
    dfview.set_color_map('normal')
    dfview.accepts_keys = [keys['down'], keys['up'], keys['left'], keys['right']]
    dfview.actions = {keys['down']: move_character_down,
                      keys['up']: move_character_up,
                      keys['left']: move_character_left,
                      keys['right']: move_character_right}
    dfview.can_accept_focus = True
    game_window.add_element(dfview)
    
def load_game_window():
    game_window.reset()
    game_window.get_focus()
   
#FIXME The block below must be replaced with actual code, of course
    
charx, chary = 10,10   

dfview = graphics.DfViewElement(0,0,graphics.width,graphics.height)
    
karte = [[field.Cell() for i in range(1000)] for j in range(1000)] 
hero = field.hero
camera = field.Camera(dfview.w, dfview.h, karte, hero)
    
def move_character_right():
    hero.x += 1
    dfview.text_map, dfview.color_map = camera.get_screen()
def move_character_left():
    hero.x -= 1
    dfview.text_map, dfview.color_map = camera.get_screen()
def move_character_up():
    hero.y -= 1
    dfview.text_map, dfview.color_map = camera.get_screen()
def move_character_down():
    hero.y += 1
    dfview.text_map, dfview.color_map = camera.get_screen()
    
    
    
    
    
    

stage_loaders = {'main window': load_main_window, 
                 'credits': load_credit_window, 
                 'new world': load_world_creation_window,
                 'game': load_game_window}
stage_unloaders = {}

create_world_creation_window()
create_game_window()
create_credit_window()
create_main_window()
