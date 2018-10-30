import numpy as np
X = np.random.rand(10,100)
y = (np.random.rand(10,4)*24+1).astype(int)
e = np.arange(100)

from generator import MyGenerator

g = MyGenerator(e, X,y,4,5,0,0.1,3)

g.get_variant1(0)
