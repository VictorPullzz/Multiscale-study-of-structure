import numpy as np
from matplotlib import pyplot as plt
from lib.utils import get_Xy

def find_CNs_index(y, CNs):
    return np.argmax((y == np.asarray(CNs)).all(axis=-1))

X_real = np.loadtxt('data/fdm_array_new.txt')
y_real = np.loadtxt('data/cns_array_new.txt')

del_ind = np.argmax(X_real.mean(axis=-1))
X_real = np.delete(X_real, del_ind, axis=0)
y_real = np.delete(y_real, del_ind, axis=0)

#X, y, E = get_Xy('data/positions/out*conv.txt')
y = y_real

freq, bins = np.histogram(y[:,0])
coef = freq.max() / freq
p = coef[np.argmax([y[:,0] < b for b in bins], axis=0) - 1]
p /= p.sum()

plt.figure('initial')
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.hist(y[:,i], bins=10)
plt.show(block=False)

samples = y[np.random.choice(len(y), 1000, p=p)]
plt.figure('resampled')
for i in range(4):
    plt.subplot(2,2,i+1)
    plt.hist(samples[:,i], bins=10)
plt.show()
