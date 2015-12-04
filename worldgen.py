import random

W=1024
MAXH=W
SCATTER=20
SL=96
WL=40
SQRT2=1.414
SEED=random.randint(1,10000)

def randint(a,b):
  r=random.random()
  r=int(r*(b-a)+a)
  return r

def square(x,y,l):
  global hmap
  x1=x+l//2
  y1=y+l//2
  hmap[x1][y1]=(hmap[x][y]+hmap[x+l][y+l]+hmap[x+l][y]+hmap[x][y+l])//4
  hmap[x1][y1]+=randint(-SCATTER*l//2,SCATTER*l//2)
  if hmap[x1][y1]<0: hmap[x1][y1]=0
  if hmap[x1][y1]>MAXH: hmap[x1][y1]=MAXH

def diamond(x,y,l):
  global hmap
  counter=0
  hmap[x][y]=0
  if x-l >= 0:
    hmap[x][y]+=hmap[x-l][y]
    counter+=1
  if x+l <= W:
    hmap[x][y]+=hmap[x+l][y]
    counter+=1
  if y-l >= 0:
    hmap[x][y]+=hmap[x][y-l]
    counter+=1
  if y+l <= W:
    hmap[x][y]+=hmap[x][y+l]
    counter+=1
  hmap[x][y]=hmap[x][y]//counter
  hmap[x][y]+=randint(-SCATTER*l//SQRT2,SCATTER*l//SQRT2)
  if hmap[x][y]<0: hmap[x][y]=0
  if hmap[x][y]>MAXH: hmap[x][y]=MAXH


def split_map(l):
  for i in range(W//l):
    for j in range(W//l):
      square(i*l,j*l,l)
  for y in range(W*2//l+1):
    for x in range(W//l+(y%2)):
      diamond(x*l+(1-y%2)*l//2,y*l//2,l//2)

def generate(size=W):
  global hmap
  global W
  global SEED
  global MAXH
  random.seed(SEED)
  hmap=[[]]
  for x in range(W+1):
    hmap+=[[]]
    hmap[x]=[]
    for y in range(W+1):
      hmap[x]+=[None]       
  l=size
  t=W
  W=size
  MAXH=W
  hmap[0][0]=randint(0,MAXH)
  hmap[0][W]=randint(0,MAXH)                 
  hmap[W][0]=randint(0,MAXH)
  hmap[W][W]=randint(0,MAXH)
  while l>1:
    split_map(l)
    l=l//2   

def export(fname='map'):
  O=open(fname,'w')
  global SEED 
  O.write(str(W)+' '+str(SEED)+'\n')
  for i in range(W+1):
    for j in range(W+1):
      O.write(str(hmap[i][j])+' ')
    O.write('\n')

def load_map(fname='map',charnum=32):
  I=open(fname,'r')
  w,seed=I.readline().split(' ')
  w,seed=int(w),int(seed) 
  hmap=[[]]
  cmap=[[]]
  for x in range(charnum):
    cmap+=[[]]
    cmap[x]=[]
    for y in range(charnum):
      cmap[x]+=[None]
  for x in range(w+1):
    hmap+=[[]]
    hmap[x]=[]
    for y in range(w+1):
      hmap[x]+=[None]
  for i in range(w+1):
      hmap[i]=I.readline().split(' ')[:-1]
      for j in range(w+1): hmap[i][j]=int(hmap[i][j])
      #print(hmap[i])      
  for i in range(charnum):
    for j in range(charnum):
      scale=w//charnum
      if scale==0: scale=1
      #print(str(w)+'//'+str(charnum)+'='+str(scale))
      s=0
      for x in range(scale):
        for y in range(scale):
          s+=hmap[i*scale+x][j*scale+y]

      s=s//(scale**2)
      s=s*100//w
      cmap[i][j]=s
  return cmap[:-1]

def map_to_strings(map):
    def what(n):
        if n>200: return 'sand'
        if n>100: return 'tree'
        if n>50: return 'floor'
        else: return 'water'
    return [[what(j) for j in i] for i in map]
    
def map_to_colors(map):
    def what(n):
        if n>200: return 'white'
        if n>100: return 'brown'
        if n>50: return 'green'
        else: return 'blue'
    return [[what(j) for j in i] for i in map]

'''generate(512)
export()
map=load_map(charnum=16)'''


