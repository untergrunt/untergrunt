# -*- coding: utf-8 -*-
import tkinter

tk=tkinter.Tk()
mg=None #Main grid, i.e. field
panel=None
#log=open('log.txt','w')
WIDTH=512
HEIGHT=512
charsize=20
AUTO_REDRAW=True
sel_reg=[]
sel_act=None
matrix=[[]]
CHARFONT='Courier New'

def void_bitmap(x,y):
  return """
  #define im_width {!s}
  #define im_height {!s}
  static char im_bits[] = """.format(x,y)+'{\n'+'0x00, '*(x*y-1)+'0x00\n}'

def inform(text):
  global panel
  for i in panel.find_all():
    panel.delete(i)
  panel.create_text(5,0,text=text,fill='white',anchor='nw',font=(CHARFONT,charsize-4))
  
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
      if self.active != i: text(x,y+h,self.text[i],size=12,fgcolor=self.def_color,align=align)
      else: text(x,y+h,self.text[i],size=12,fgcolor=self.act_color,align=align)
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

def change_resolution(dpi):
  global charsize
  charsize=dpi
  #fill('#')

def init_screen():
  global tk
  global mg
  global panel
  tk.title("Game screen")
  mg=tkinter.Canvas(tk,height=HEIGHT,width=WIDTH,background='#000000',borderwidth=0)
  mg.pack()
  panel=tkinter.Canvas(tk,height=charsize+6,width=WIDTH,background='#000000',borderwidth=0)
  panel.pack()

def symbol(x,y,c,color='white'):
  global mg,matrix
  if matrix==[[]]: fill(' ')
  mg.delete(matrix[x][y])
  mg.create_rectangle(x*charsize-1,y*charsize,(x+1)*charsize,(y+1.2)*charsize,fill='black')
  if c not in [',','_']: matrix[x][y]=mg.create_text((x+0.5)*charsize,(y+0.5)*charsize,text=c,fill=color,font=(CHARFONT,charsize-2))
  else: matrix[x][y]=mg.create_text((x+0.5)*charsize,(y+0.2)*charsize,text=c,fill=color,font=(CHARFONT,charsize))

def fill(c,color='white'):
  global matrix,tk
  matrix=[[]]
  for i in range(5):
    for j in range(5):
      a=tkinter.Label(tk,text='text')
      a.pack()
  for i in range(int(WIDTH/charsize)):
    matrix+=[[]]
    for j in range(int(HEIGHT/charsize)):
      matrix[i]+=[mg.create_text((i+0.5)*charsize,(j+0.2)*charsize,text=c,fill=color,font=(CHARFONT,charsize))]

def wipe():
  global mg
  #mg.create_rectangle(0,0,WIDTH,HEIGHT,fill='black')
  for i in mg.find_all():
    mg.delete(i)

def text(x,y,text,fgcolor='white',bgcolor='black',font=CHARFONT,size=12,align='w'):
  global mg
  if align=='w': r=mg.create_rectangle(x,y-size/2+1,x+len(text)*(size-2),y+size/2+1,fill='black')
  elif align=='c': r=mg.create_rectangle(x-len(text)*(size-2)//2,y-size/2+1,x+len(text)*(size-2)//2,y+size/2+1,fill='black')
  t=mg.create_text(x,y,text=text,anchor=align,fill=fgcolor,font=(font,size))
  return (t,r)

def report():
  global panel
  panel.create_text(5,30,text='Report',font=(CHARFONT,12),fill='red',anchor='w')

def frame(title):
  global mg
  wipe()
  mg.create_rectangle(10,10,WIDTH-7,HEIGHT-7,outline='white')
  charsize=12
  mg.create_rectangle(int(WIDTH/2-len(title)/2*charsize),2,int(WIDTH/2+len(title)/2*charsize),charsize,fill='black')
  mg.create_text(int(WIDTH/2),charsize,text=title,fill='white',font=(CHARFONT,charsize))

def I_AM_NOT_GOING_TO_CREATE_OBJECTS_AFTER_THIS(main):
  global tk
  #w0=window(0,0,WIDTH,HEIGHT,'black')
  #w1=window(100,20,50,25)
  #w0.show()
  #w1.show()
  #w1.hide()
  #void_bitmap(3,4)
  main()
  tk.mainloop()
      