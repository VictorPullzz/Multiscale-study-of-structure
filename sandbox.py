import numpy as np
from matplotlib import pyplot as plt
from lib.utils import get_Xy
from lib.generator import DataAugmentator

def find_CNs_index(y, CNs):
    return np.argmax((y == np.asarray(CNs)).all(axis=-1))

X_real = np.loadtxt('data/fdm_array_new.txt')
y_real = np.loadtxt('data/cns_array_new.txt')

del_ind = np.argmax(X_real.mean(axis=-1))
X_real = np.delete(X_real, del_ind, axis=0)
y_real = np.delete(y_real, del_ind, axis=0)

X, y, E = get_Xy('data/positions/out*conv.txt')

da = DataAugmentator(X_real, y_real, True, 256)
# for item in da.__getitem__(0):
#     print(item[1])
samples = da.__getitem__(0)[1]
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.hist(samples[:,i], bins=10)
plt.show()
