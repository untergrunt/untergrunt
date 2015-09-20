
from sys import stdout
stdout=open('log.txt','w')
import very_new_forms as f
import creatures as c
import humanoids as c_h
import worldgen as w
import engine as e
from random import randint as rand

mode=None
from sys import stdout
stdout=open('log.txt','w')
L_LOWER=['a']
L_UPPER=['A']
for i in range(25):
  L_LOWER+=[chr(ord(L_LOWER[i])+1)]
  L_UPPER+=[chr(ord(L_UPPER[i])+1)]
f.texts=['Message','Some other message','Blood to the god of blood!','ASCII kills','etc']
KEY={'left':37,'right':39,'up':38,'down':40,'enter':13,'upz':188,'downz':190}
form={'race':'human','name':'Marcus'}
hero=None
M=None
camera=(0,0,0)                   #UL corner

class TimeMachine:
  time=0
  events=[] #element=[period,time,function]
  def __init__(self):
    self.time=0
  def go(self,t):
   tt=self.time+t
   if len(self.events):
    while self.time<tt:
      f=0
      events=self.events
      print(events)
      for i in range(len(events)):
        if (events[i][0]-events[i][1]<events[f][0]-events[f][1]): f=i
      dt=min(events[f][0]-events[f][1],tt-self.time)
      if len(events):
        self.time+=dt
      for i in range(len(events)):
        events[i][1]+=dt
        if events[i][1]>=events[i][0]:
          #print('Local time was {!s}, dt is {!s}'.format(events[i][1],dt)) 
          events[i][1]-=events[i][0]
          #print('Now local time is {!s}'.format(events[i][1]))
          events[i][2]()

T=TimeMachine()
                                                                                                                          
def alert(text):
  global mode
  l=len(text)
  txt=[]
  while l*f.charsize//2+200>f.WIDTH:
    l-=(f.WIDTH-200)*2//f.charsize
    txt+=[text[:(f.WIDTH-200)*2//f.charsize]]
    text=text[(f.WIDTH-200)*2//f.charsize:]
  if len(txt)!=0: txt+=[text]
  if len(txt)==0: 
    r=f.scr.create_rectangle((f.WIDTH-len(text)*f.charsize//2)//2-50,f.HEIGHT//2-20,(f.WIDTH+len(text)*f.charsize//2)//2+50,f.HEIGHT//2+20,fill='black',outline='white')
    t=f.text(f.WIDTH//2,f.HEIGHT//2,text,align='c')
  else:
    r=f.scr.create_rectangle((f.WIDTH-len(txt[0])*f.charsize//2)//2-50,f.HEIGHT//2-20,(f.WIDTH+len(txt[0])*f.charsize//2)//2+50,f.HEIGHT//2+20+f.charsize*len(txt),fill='black',outline='white')
    for i in range(len(txt)):
      t=f.text(f.WIDTH//2,f.HEIGHT//2+f.charsize*i,txt[i],align='c')  
  mode=['alert',r,t,mode]

def roll_character():
  global hero
  global form
  hero=c.Creature(c.race_by_name[form['race']],form['name'],'@')

def enter_battle_mode():
  f.change_mode('symbols')
  f.wipe()
  global mode
  global hero
  global M
  M=e.Karte.generate_map()
  mode='battle'
  hero.glob_coord=form['coord']
  x,y=0,0
  z=0
  while M.get(x,y,z).mat!='air': 
    z+=1
  hero.coord=(x,y,z)
  for x in range(f.W):
    for y in range(f.H):
      f.symbol(x,y,M.get(x+camera[0],y+camera[0],hero.coord[2]-1).sym)
  f.symbol(20,20,'@')

def move_hero(d):
  global hero,M,T
  if d==KEY['left']:
    hero.coord=(hero.coord[0]-1,hero.coord[1],hero.coord[2])
  elif d==KEY['right']:
    hero.coord=(hero.coord[0]+1,hero.coord[1],hero.coord[2])
  elif d==KEY['up']:
    hero.coord=(hero.coord[0],hero.coord[1]-1,hero.coord[2])
  elif d==KEY['down']:
    hero.coord=(hero.coord[0],hero.coord[1]+1,hero.coord[2])
  elif d==KEY['upz']:
    hero.coord=(hero.coord[0],hero.coord[1],hero.coord[2]+1)
  elif d==KEY['downz']:
    hero.coord=(hero.coord[0],hero.coord[1],hero.coord[2]-1)
  f.inform('Hero coords are: '+str(hero.coord))   
  T.go(1000)
  #f.scr.place(x=0,y=0)
  for x in range(f.W):
    for y in range(f.H):
      f.symbol(x,y,M.get(x+camera[0]+hero.coord[0],y+camera[1]+hero.coord[1],hero.coord[2]-1).sym)
  f.symbol(f.W//2,f.H//2,'@')
  #f.scr.place(x=500,y=500)

def keypress(event):                               
  x=event.char
  global mode
  #print(event.keycode)
  if mode=='start':
    if x in ['q','Q']: exit()
    elif x in L_LOWER+L_UPPER: 
      #symbol(5,10,x,'red')
      #enter_start_mode()
      pass
    if (event.keycode==KEY['down'])&(f.sel_act!=None): f.sel_act.down()
    elif (event.keycode==KEY['up'])&(f.sel_act!=None): f.sel_act.up()
    elif (event.keycode==KEY['enter'])&(f.sel_act!=None): f.sel_act.enter()  
    elif event.keycode==KEY['left']: f.selector.left()
    elif event.keycode==KEY['right']: f.selector.right()
  elif mode=='credits': enter_start_mode()
  elif mode=='battle':                                        
    if event.keycode in [KEY['down'],KEY['up'],KEY['left'],KEY['right'],KEY['upz'],KEY['downz']]:
      move_hero(event.keycode)
  elif mode[0]=='alert':
    if event.keycode==KEY['enter']: 
      f.scr.delete(mode[1],mode[2][0],mode[2][1])
      mode=mode[3]
  elif mode=='roll':
    if event.keycode==8: enter_start_mode()
    elif (event.keycode==KEY['down'])&(f.sel_act!=None): f.sel_act.down()
    elif (event.keycode==KEY['up'])&(f.sel_act!=None): f.sel_act.up()
    elif (event.keycode==KEY['enter'])&(f.sel_act!=None): f.sel_act.enter()  
    elif event.keycode==KEY['left']: f.selector.left()
    elif event.keycode==KEY['right']: f.selector.right()
    elif x=='s':
      roll_character()
      enter_battle_mode()
  else: enter_start_mode()

def rand_elem(arr):
  return arr[rand(0,len(arr)-1)]

def main_menu_agent(option):
  global mode
  if option=='Quit': exit()
  elif option=='New game': 
    enter_roll_mode()
    #alert('Roll your character!')
  elif option=='Continue game':
    f.fill(' ')
    for i in range(10,21):
      f.symbol(i,10,'#')
      f.symbol(i,20,'#')
      f.symbol(10,i,'#')
      f.symbol(20,i,'#')
    for i in range(11,20):
      for j in range(11,20): f.symbol(i,j,'+')
    f.symbol(15,15,'@')
    mode='battle'
  elif option=='Create new world': enter_worldgen_mode()
  elif option=='Credits':
    f.frame(title='Credits menu')
    f.text(100,200,'All hail Andrei Pago!')
    mode='credits'

def enter_start_mode():
  global scr
  global mode
  f.change_mode('window')
  f.wipe()
  mode='start'
  f.selector.wipe()
  f.frame('Welcome! I wish you die happily!')
  global main_menu
  main_menu=f.selector(['New game','Continue game','Create new world','Credits','Quit'],main_menu_agent,align='c',def_color='gray',act_color='red')
  main_menu.activate(f.WIDTH/2,f.HEIGHT/2-100)
  main_menu.focus(0)

def enter_worldgen_mode():
  global mode
  mode='worldgen'
  f.change_mode('symbols')
  f.wipe()
  w.generate(512)
  w.export()
  map=w.load_map(charnum=min(f.W,f.H))
  for y in range(len(map)):
    for x in range(len(map[y])):
      c=map[x][y]
      if c>90:
        f.symbol(x,y,'^',color='white')
      elif c<40:
        f.symbol(x,y,'~',color='blue')
      elif c>60:
        f.symbol(x,y,'v',color='brown')
      else:
        f.symbol(x,y,'+',color='green')

def race_choice_agent(option):
  #print('Your race is now '+option)
  hero.race.name=option
  print(hero.describe())
def god_choice_agent(option):
  print('Your god is now '+option)

def enter_roll_mode():
  global scr
  global mode
  global form
  mode='roll'
  f.change_mode('window')
  f.wipe()
  f.frame('Roll your character')
  f.selector.wipe()
  f.text(20,50,'Choose your race:',fg='green',size=12)
  race_choice=f.selector(['human','orc','dwarf','elf','half-troll'],race_choice_agent)
  race_choice.activate(20,75)
  race_choice.focus(0)
  map=w.load_map()
  c=[rand(0,31),rand(0,31)]
  form['coord']=c
  #f.inform('Your coordinates are: '+str(c))
  while (map[c[0]][c[1]]<40)|(map[c[0]][c[1]]>90): c=[rand(0,31),rand(0,31)]
  f.text(220,50,'Starting location:',fg='blue',size=12)
  f.text(240,80,'('+str(c[0])+','+str(c[1])+')',size=12)
  f.text(50,f.HEIGHT-50,"Press 's' to start...",fg='yellow',size=12)
  if map[c[0]][c[1]]<60:
    f.symbol(230//f.charsize,70//f.charsize+1,'+',color='green')
  else:
    f.symbol(230//f.charsize,70//f.charsize+1,'v',color='brown')
                                                               
def main():
  enter_start_mode()
  global hero
  hero=c.Creature(c_h.human_race,'Marcus','@')
  f.app.bind_all('<Key>',keypress)

f.t(main)
#f.I_AM_NOT_GOING_TO_CREATE_OBJECTS_AFTER_THIS(main)