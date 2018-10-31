import numpy as np
from matplotlib import pyplot as plt

def find_CNs_index(y, CNs):
    return np.argmax((y == np.asarray(CNs)).all(axis=-1))

X_real = np.loadtxt('data/fdm_array_new.txt')
y_real = np.loadtxt('data/cns_array_new.txt')

del_ind = np.argmax(X_real.mean(axis=-1))
X_real = np.delete(X_real, del_ind, axis=0)
y_real = np.delete(y_real, del_ind, axis=0)

for i in range(4):
    plt.subplot(2,2,i+1)
    plt.hist(y_real[:,i], bins=np.linspace(y_real[:,i].min(), y_real[:,i].max(), 30))
plt.show()
