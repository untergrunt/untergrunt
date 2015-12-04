from mapgen import *

a = BigMap('plane',9,9,5)
a.generate()
print(a.get_update(1,1) == a.get_update(5,5))
