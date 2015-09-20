race_by_name={}

class Bodypart:
  size=0
  hp=0
  name=''
  def __init__(self,size,name,hp):
    self.size=size
    self.hp=hp
    self.name=name
  def copy(self):
    result=Bodypart(self.size,self.hp)
    return result

bp=Bodypart

class Body:
  links=[]
  parts=[]
  pn={}
  def describe(self):
    print('This body consists of '+str(len(self.parts))+' bodyparts:')
    a=''
    for i in self.parts: a+=', '+i.name
    a=a[2:]
    print(a)
    for link in self.links:
      print(link[0].name+' and '+link[1].name+' are joined')
  def __init__(self,parts,links):
    self.parts=parts
    for part in parts:
      self.pn[part.name]=part
    self.links=links
  def copy(self):
    result=Body([],[])
    for part in self.parts: result.parts+=[part]
    for link in self.links: result.links+=[link]
    for part in self.parts: self.pn[part.name]=part
    return result

class Race:
  name,body,symbol=[None]*3
  def __init__(self,name,symbol,racebody):
    self.name=name
    self.symbol=symbol
    self.body=racebody
    race_by_name[name]=self

class Creature:
  race,name,symbol,body,size=[None]*5
  coord,glob_coord=(0,0,0),(0,0)
  def __init__(self,race,name,symbol=None):
    self.race=race
    self.name=name
    self.symbol=symbol
    if self.symbol==None: self.symbol=self.race.symbol
    #print(self.race.symbol)
    self.body=self.race.body.copy()
    self.size=0
    for part in self.body.parts: self.size+=part.size
  def describe(self):
    result=self.symbol+': This is a '+self.race.name+', whose name is '+self.name+'\n'
    result+="It's size is "+str(self.size)
    return result
  def locate_globally(self,x,y):
    self.glob_coord=(x,y)
  def locate_locally(self,x,y,z):
    self.coord=(x,y,z)
















                                      