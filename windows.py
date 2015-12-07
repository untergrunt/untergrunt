import graphics
import worldgen
import field
from materials import Material, Water, Sand, Air, Stone, Void, Dirt
from tiles import *
import camera
from mechanics import player_acts

by_name = Material.by_name

print = graphics.print

current_stage = 'main window'

keys = graphics.keys

MSG = graphics.MessageBox

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

def create_main_window():
    main_window.wipe()
    title_text = graphics.LabelElement(graphics.width//2-7, 5,'THE ROGUELIKE!','br')
    buttons = [
    ('New game', lambda: change_stage('game')),
    ('Create new world', lambda: print('Disabled')),
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
    t1 = graphics.LabelElement(10, 10, 'Thanks to:', style='br')
    t2 = graphics.LabelElement(10, 13, 'The game is not nearly ready, so no credits for now', style='')
    t3 = graphics.LabelElement(10, 14, 'Not sure if I need them anyway...', style='')
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
    global karte, big_brother
    short_text = 'The forgotten beast Afjbskfb has arrived! It has four wings and its eyes glow red. Beware its poisonous gas!'
    def return_back():
        inventory_window.hide()
        game_window.get_focus()
    inventory_window = graphics.Window(0,0, graphics.width, graphics.height, title='Inventory', style='', back=return_back)
    dic = {keys['i']: lambda: inventory_window.get_focus(),
           keys['enter']: lambda: MSG.pop(short_text, game_window)}
    kae = graphics.KeyAcceptorElement(dic)
    karte = camera.BigMap('dungeon',3000,3000)
    karte.add_creature(hero, 1500, 1500)
    big_brother = camera.Camera(dfview.w, dfview.h, karte, hero)
    game_window.add_element(kae)
    global locator
    locator = graphics.LabelElement(1,1,'(500, 500)')
    global dfview
    dfview.set_text_map('.')
    dfview.set_color_map('normal')
    dfview.accepts_keys = [keys['down'], keys['up'], keys['left'], keys['right']]
    dfview.actions = {
        keys['down']: lambda:player_really_acts('down'),
        keys['up']: lambda:player_really_acts('up'),
        keys['left']: lambda:player_really_acts('left'),
        keys['right']: lambda:player_really_acts('right')
    }
    dfview.can_accept_focus = True
    game_window.add_element(dfview)
    game_window.add_element(locator)
    
def load_game_window():
    global karte, info, big_brother
    game_window.reset()
    '''def generate_local_map_of_materials(map_of_things):
        m=map_of_things
        dic = {
            'water': Water,
            'stone': Stone,
            'air': Air,
            'void': Void,
            'sand': Sand,
            'tree': Stone,
            'floor': Dirt
        }
        return [[field.Cell(dic[map_of_things[j][i]]) for i in range(1024)] for j in range(1024)]'''
    '''Map initialization'''
    karte.generate()
    karte.add_creature(hero, 1500, 1500)
    from hero import gob
    karte.add_creature(gob, 1505, 1504)
    karte.hero = hero
    '''End map init '''
    game_window.get_focus()
    dfview.text_map, dfview.color_map = big_brother.get_screen()
   
#FIXME The block below must be replaced with actual code, of course
#HA-HA, replaced
  
MSG.back = game_window
    
charx, chary = 10,10   

dfview = graphics.DfViewElement(0,0,graphics.width,graphics.height)


hero = field.hero


    
    
def player_really_acts(event):
    player_acts(event, karte)
    dfview.text_map, dfview.color_map = big_brother.get_screen()
    locator.text = str(big_brother.field.where_is(hero))
    
    
    

stage_loaders = {'main window': load_main_window, 
                 'credits': load_credit_window, 
                 'new world': load_world_creation_window,
                 'game': load_game_window}
stage_unloaders = {
'main window': lambda: main_window.hide(),
'credits': lambda: credit_window.hide(),
'new world': lambda: world_creation_window.hide(),
'game': lambda: game_window.hide()
}

create_world_creation_window()
create_game_window()
create_credit_window()
create_main_window()
