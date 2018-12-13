import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from keras.layers.core import Dropout
from keras.callbacks import TensorBoard as TB, ModelCheckpoint as MCP, EarlyStopping as ES
from keras import regularizers
import os
from lib.utils import get_Xy
from lib.generator import MyGenerator
from lib.nn import get_model, random_seed

random_seed(42)

def loadreal(spectra, cns):
    X_real = np.loadtxt(spectra)
    y_real = np.loadtxt(cns)
    #X_real = X_real / np.max(X_real, axis=-1)[:,None]
    #X_real = X_real[:,1:] - X_real[:,:-1]
    #y_real = y_real / np.array([12,6,24,12])
    X_train_real, X_test_real, y_train_real, y_test_real = train_test_split(X_real, y_real, test_size=0.33, random_state=42)
    return X_train_real, X_test_real, y_train_real, y_test_real

def view_pred(X, y):
    y_pred = model.predict_on_batch(X)
    for i, k in enumerate([12,6,24,12]):
        plt.subplot(2,2,i+1)
        plt.plot(np.arange(0.,1.1,0.1)*k,np.arange(0.,1.1,0.1)*k, 'r-')
        plt.scatter(y[:,i]*k, y_pred[:,i]*k)
    plt.show()
    return y_pred

X_train_real, X_test_real, y_train_real, y_test_real = loadreal('data/fdm_array_new.txt', 'data/cns_array_new.txt')

model = get_model()
model.summary()

model_backup_name = 'model2.hd5'

X, y, E = get_Xy('data/positions/out*conv.txt')

train_gen = MyGenerator(E,X[:80],y[:80],3,10,1,0.05,256, mode='variant1')
val_gen   = MyGenerator(E,X[80:],y[80:],3,10,1,0.05,256, mode='variant1')

if (True):
    model.fit_generator(train_gen,
                        validation_data=val_gen,
                        steps_per_epoch=200,
                        epochs=200,
                        callbacks=[MCP(model_backup_name, save_best_only=True),
                                   ES(patience=15, verbose=True),
                                   TB()
                                   ]
                        )
model.load_weights(model_backup_name)

X_val, y_val = val_gen.__getitem__(0)
y_pred = view_pred(X_val, y_val)
np.set_printoptions(precision=1)
for X_, y_, p_ in zip(X_val[:5], y_val[:5], y_pred[:5]):
    plt.plot(np.cumsum(X_), label=y_*np.asarray([12,6,24,12]))
    print(p_*np.asarray([12,6,24,12]))
plt.legend()
plt.show()

X_val, y_val = MyGenerator(E,X_test_real,y_test_real,1,2,1,0.05,256).__getitem__(0)
y_pred = view_pred(X_val, y_val)
