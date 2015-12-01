import tkinter as TK
W,H=40,21
charsize=14
WIDTH=W*(charsize-1)
HEIGHT=H*(charsize+4)+20
screen=[[]]
panel=None
graph_mode='window'
CHARFONT='Courier New'
sel_reg=[]
sel_act=None


app=TK.Tk()
app.geometry(str(WIDTH)+'x'+str(HEIGHT))
app['bg']='black'

scr=None

for x in range(W):
  screen+=[[]]
  for y in range(H):
    screen[x]+=[None]

def inform(text):
  global panel
  panel['text']=text

def change_mode(m):
  global graph_mode,screen,scr
  if m!=graph_mode:
    graph_mode=m
    if m!='symbols': 
      scr.place(x=0,y=0)
    else:
      scr.place(x=WIDTH+100,y=HEIGHT+100)
  wipe()     

def text(x,y,text,fg='white',bg='black',font=CHARFONT,size=charsize,align='nw'):
  if graph_mode=='symbols':
    for i in range(x,min(x+len(text),W)): 
      symbol(i,y,text[i-x])
  elif graph_mode=='window':
    if align=='w': r=scr.create_rectangle(x,y-size/2+1,x+len(text)*(size-2),y+size/2+1,fill=bg)
    elif align=='c': r=scr.create_rectangle(x-len(text)*(size-2)//2,y-size/2+1,x+len(text)*(size-2)//2,y+size/2+1,fill=bg)
    t=scr.create_text(x,y,text=text,anchor=align,fill=fg,font=(font,size))
        

def init_screen():
  global app,charsize,screen,panel,scr
  panel=TK.Label(app,text='Info panel',font=('Arial',12),bg='black',fg='white',borderwidth=0)
  panel.place(x=0,y=HEIGHT-18)
  app.title("Game screen")
  for x in range(W):
    for y in range(H):
      screen[x][y]=TK.Label(app,text='!',font=('Courier New',charsize),bg='black',fg='white',borderwidth=0)
      screen[x][y].place(x=x*(charsize-1),y=y*(charsize+4))
  scr=TK.Canvas(app,height=HEIGHT-20,width=WIDTH,background='#000000')
  if graph_mode=='window': scr.place(x=0,y=0)
      
def fill(txt):
  global screen
  for x in range(W):
    for y in range(H):
      screen[x][y]['text']=txt

def symbol(x,y,txt,color='white'):
  if graph_mode=='symbols':
    global screen
    #print(str(x)+' '+str(y))
    screen[x][y]['fg']=color
    screen[x][y]['text']=txt
  elif graph_mode=='window':
    global scr
    scr.create_rectangle(x*charsize-1,y*charsize,(x+1)*charsize,(y+1.2)*charsize,fill='black')
    if txt not in [',','_']: scr.create_text((x+0.5)*charsize,(y+0.5)*charsize,text=txt,fill=color,font=(CHARFONT,charsize-2))
    else: scr.create_text((x+0.5)*charsize,(y+0.2)*charsize,text=txt,fill=color,font=(CHARFONT,charsize))


def frame(title):
 global scr,graph_mode
 if graph_mode=='window':
  scr.create_rectangle(10,10,WIDTH-7,HEIGHT-27,outline='white')
  scr.create_rectangle(int(WIDTH/2-len(title)/2*charsize),2,int(WIDTH/2+len(title)/2*charsize),charsize,fill='black')
  scr.create_text(int(WIDTH/2),charsize,text=title,fill='white',font=(CHARFONT,charsize))
 elif graph_mode=='symbols':
  for i in range(W):
   symbol(i,0,'-')
   symbol(i,H-1,'-')
  for i in range(H):
   symbol(0,i,'|')
   symbol(W-1,i,'|')
  symbol(0,0,'+')
  symbol(0,H-1,'+')
  symbol(W-1,0,'+')
  symbol(W-1,H-1,'+')
  text((W-len(title))//2,0,title)

def report(txt):
  global panel     
  panel['text']=txt

def wipe():
  if graph_mode=='symbols':
    for x in range(W):
      for y in range(H):
        symbol(x,y,' ')
  elif graph_mode=='window':
    for i in scr.find_all(): scr.delete(i)

'''def keypress(e):
 if graph_mode=='window':
  change_mode('symbols')
  #text(0,1,'==================TITLE==================')
  frame('Title')
  report('Title has been created in symbols mode')
 else:
  change_mode('window')
  frame('Title')
  report('Title has been created in window mode')'''

class selector:
  text=[]
  agent=None
  active=None
  visible=True
  x,y=50,50
  align='w'
  def_color='white'
  act_color='gray'
  def __init__(self,texts,agent,align='w',def_color='gray',act_color='white'):
    self.align=align
    self.text=texts
    self.agent=agent
    self.act_color=act_color
    self.def_color=def_color
    global sel_reg
    sel_reg+=[self]
  def locate(self,x,y):
    self.x,self.y=x,y
  def print(self,x=None,y=None,align=None):
    h=0
    if align==None: align=self.align
    if x==None:x=self.x
    if y==None:y=self.y
    self.visible=True
    for i in range(len(self.text)):
      if self.active != i: text(x,y+h,self.text[i],size=12,fg=self.def_color,align=align)
      else: text(x,y+h,self.text[i],size=12,fg=self.act_color,align=align)
      h+=15
  def activate(self,x=None,y=None,align=None):
    global sel_act
    if align==None:align=self.align
    sel_act=self
    self.visible=True
    if (x==None)|(y==None): self.print(align=align)
    else: 
      self.locate(x,y)
      self.print(align=align)
  def focus(self,num):
    self.active=num
    if self.visible: self.print(self.x,self.y)
  def up(self):
    if self.active is None: self.active=0
    elif self.active==0: self.active=len(self.text)-1
    else: self.active-=1
    if self.visible: self.print()
  def down(self):
    if self.active is None: self.active=0
    elif self.active==len(self.text)-1: self.active=0
    else: self.active+=1
    if self.visible: self.print()
  def enter(self):
    if self.active is not None:
      if self.agent is not None: 
        self.agent(self.text[self.active])  
  def off(self):
    self.active=None
    if self.visible: self.print()
  def on(self):
    self.focus(0)
  def wipe():
    global sel_reg
    global sel_act
    global mg     
    sel_reg=[]
    sel_act=None
  def left():
    global sel_act
    global sel_reg
    if sel_reg!=[]:
     g=sel_reg.index(sel_act)
     flag=True
     for g in reversed(range(g)):
      if sel_reg[g].visible:
       sel_act.off()
       sel_act=sel_reg[g]
       sel_act.on()
       flag=False
       break
     if flag:
      for g in reversed(range(g,len(sel_reg))):
       if sel_reg[g].visible:
        sel_act.off()
        sel_act=sel_reg[g]
        sel_act.on()
        break
  def right():
    global sel_act
    global sel_reg
    if sel_reg!=[]:
     g=sel_reg.index(sel_act)
     flag=True
     for g in range(g+1,len(sel_reg)):
      if sel_reg[g].visible:
       sel_act.off()
       sel_act=sel_reg[g]
       sel_act.on()
       flag=False
       break
     if flag:
      for g in range(g+1):
       if sel_reg[g].visible:
        sel_act.off()
        sel_act=sel_reg[g]
        sel_act.on()
        break

def t(main):
  init_screen()
  main()
  app.mainloop()

