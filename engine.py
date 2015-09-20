import worldgen as w
import creatures as c
from random import randint

MAP_W=100
MAP_H=100

mat_symbol={'air':' ','stone':'#','grass':','}

class Tile:
  mat=None
  sym=None
  def __init__(self,material):
    self.mat=material
    self.sym=mat_symbol[material]
  def tostr(self):
    return self.mat

class Karte:
  layers=[]
  def __init__(self):
    for z in range(MAP_H):
      self.layers+=[[]]
      for x in range(MAP_W):
        self.layers[z]+=[[]]
        for y in range(MAP_W):
          self.layers[z][x]+=[Tile('stone')]
  def get(self,x,y,z):
    return self.layers[z][x][y]
  def set(self,x,y,z,tile):
    self.layers[z][x][y]=tile
  def generate_map():
    k=Karte()
    for i in range(MAP_H//2):
      for j in range(MAP_W):
        for l in range(MAP_W): k.set(j,l,i,Tile(['stone','grass'][randint(0,1)]))
    for i in range(MAP_H//2,MAP_H):
      for j in range(MAP_W):
        for l in range(MAP_W): k.set(j,l,i,Tile('air'))
    return k
  def print(self):
    for i in range(len(self.layers)):
      print('Layer '+str(i))
      for j in self.layers[i]: p(j)
        


