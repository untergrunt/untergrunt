import graphics
import worldgen
import field
import camera
from mechanics import player_acts
from creatures import Creature

ascii = camera.ascii

print = graphics.print

keys = graphics.keys

MSG = graphics.MessageBox

height, width = graphics.height, graphics.width

current_stage = 'main window'

def change_stage(new_stage):
    global current_stage
    if current_stage in stage_unloaders:
        stage_unloaders[current_stage]()
    assert(new_stage in stage_loaders)
    stage_loaders[new_stage]()
    current_stage = new_stage

main_window = graphics.Window(0, 0, width, height, title='Main menu', style='n')
game_window = graphics.Window(0, 0, width, height, title='Game window', style='n', back=lambda:change_stage('main window'))
credit_window = graphics.Window(0, 0, width, height, title='Credits', back=lambda:change_stage('main window'), style='n')
world_creation_window = graphics.Window(0, 0, width, height, title='', back=lambda:change_stage('main window'), style='n')

def create_main_window():
    main_window.wipe()
    title_text = graphics.LabelElement(width//2-7, 5,'THE ROGUELIKE!','br')
    buttons = [
        ('New game', lambda: change_stage('game')),
        ('Create new world', lambda: print('Disabled')),
        ('Load game', lambda: print('New game loaded')),
        ('Show credits', lambda: change_stage('credits')),
        ('Quit', graphics.die)
    ]
    vmenu = graphics.VerticalMenuElement(width//3, 10, buttons)
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
    global karte
    global big_brother
    global locator
    global dfview
    global hero
    MSG.back = game_window
    hero = field.hero
    dfview = graphics.DfViewElement(0, 0, width, height)
    short_text = \
        'The forgotten beast Afjbskfb has arrived! It has four wings and its eyes glow red. Beware its poisonous gas!'
    dic = {
            keys['i']: lambda: inventory_window.get_focus(),
            keys['k']: lambda: cursor.get_focus(),
            keys['enter']: lambda: MSG.pop(short_text)
          }
    kae = graphics.KeyAcceptorElement(dic)
    
    def return_back():
        inventory_window.hide()
        game_window.get_focus()
        
    inventory_window = graphics.Window(0,0, width, height, title='Inventory', style='', back=return_back)
    karte = camera.BigMap('dungeon',1000,1000)
    locator = graphics.LabelElement(1,1,'(500, 500)')
    karte.add_creature(hero, 500, 500)
    big_brother = camera.Camera(dfview.w, dfview.h, karte, hero)
    def handler(self, x, y):
        cre = karte.get_creatures()
        g_x, g_y = big_brother.to_global((x, y))
        #s = ['floor: {}\nfill: {}\ncoords: ({}, {})'.format(karte.m[g_y][g_x].floor.name, karte.m[g_y][g_x].fill.name, g_x, g_y)]
        s=[]
        cell=karte.m[g_y][g_x]
        for k in cre:
            if big_brother.to_local(cre[k]) == (x, y):
                s += ['Here you see a {} standing on {} surrounded by {}'.format(Creature.by_id(k).race.name, cell.floor.name, cell.fill.name)]
        s = '\n'.join(s)
        if s == '':
            s = 'The floor is {}, the fill is {}'.format(cell.floor.name, cell.fill.name)
        MSG.pop(s)
        
    cursor = graphics.CursorElement(0, 0, width-1, height-1, handler)
    
    def setup_dfview():
        dfview.accepts_keys = [keys['down'], keys['up'], keys['left'], keys['right'], keys['.']]
        dfview.actions = {
            keys['down']: lambda:let_the_player_act_and_pass_the_changes_to_the_dfview('down'),
            keys['up']: lambda:let_the_player_act_and_pass_the_changes_to_the_dfview('up'),
            keys['left']: lambda:let_the_player_act_and_pass_the_changes_to_the_dfview('left'),
            keys['right']: lambda:let_the_player_act_and_pass_the_changes_to_the_dfview('right'),
            keys['.']: lambda:let_the_player_act_and_pass_the_changes_to_the_dfview('wait')
        }
        dfview.can_accept_focus = True
        
    setup_dfview()
    game_window.wipe()
    game_window.add_element(kae)
    game_window.add_element(dfview)
    game_window.add_element(locator)
    game_window.add_element(cursor)
    
def load_game_window():
    global karte, info, big_brother
    from hero import gob
    '''Map initialization'''
    karte.generate()
    karte.add_creature(hero, 500, 500)
    karte.add_creature(gob, 505, 504)
    karte.hero = hero
    '''End map initializasion '''
    game_window.reset()
    game_window.get_focus()
#    big_brother.actor = gob #For fun
    dfview.text_map, dfview.color_map = big_brother.get_screen()
    
    
def let_the_player_act_and_pass_the_changes_to_the_dfview(player_action):
    player_acts(player_action, karte)
    dfview.text_map, dfview.color_map = big_brother.get_screen()
    locator.text = str(big_brother.field.where_is(hero))
        
    

stage_loaders = {
                 'main window': load_main_window, 
                 'credits': load_credit_window, 
                 'new world': load_world_creation_window,
                 'game': load_game_window
                }
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
