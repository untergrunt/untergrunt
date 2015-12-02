v_letters=('a','e','i','o','u','y')

class Thing:
  p={}  #properties
  name=''
  def __init__(self,name,properties):
    self.name=name
    self.p=properties
  def description(self):
    adj=''
    has_n=['','n'][self.name[0].lower() in v_letters]
    if '_adjective' in self.p.keys():
      adj=self.p['_adjective']
      has_n=[' ','n '][adj[0].lower() in v_letters]
    s='This is a'+has_n+adj+' '+self.name
    for p in self.p.keys():
      if p[0]!='_':
        s+='\nIts '+str(p)+' is '+str(self.p[p])
    return s

a=Thing('English sword',{'sharpness':30,'mass':'10kg','material':'iron','quality':'high','_adjective':'great','symbol':'-'})
print(a.description())

