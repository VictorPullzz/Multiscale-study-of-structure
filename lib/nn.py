from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D, Reshape, Dropout
from keras.models import Sequential
from tensorflow import set_random_seed
import keras.backend as K
import numpy as np

def random_seed(seed):
    np.random.seed(42)
    set_random_seed(42)

def weighted_mse(weights=[12,6,24,12]):
    def loss(y_true, y_pred):
        return K.mean(K.square((y_pred - y_true))*np.asarray(weights), axis=-1)
    return loss

def get_model():
    model = Sequential()
    # model.add(Reshape((94, 1), input_shape=(94,)))
    # model.add(Conv1D(16, 5, init='he_uniform', padding='same', activation='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Conv1D(32, 5, init='he_uniform', padding='same', activation='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Conv1D(64, 5, init='he_uniform', padding='same', activation='relu'))
    # model.add(MaxPooling1D(2))
    # model.add(Dropout(0.5))
    # model.add(Flatten())
    # model.add(Dense(64, activation='relu'))
    # model.add(Dense(4,  activation='sigmoid'))
    model.add(Reshape((94, 1), input_shape=(94,)))
    model.add(Conv1D(32, 5, init='he_uniform', padding='same', activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(32, 5, init='he_uniform', padding='same', activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(32, 5, init='he_uniform', padding='same', activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Conv1D(32, 5, init='he_uniform', padding='same', activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(32, activation='relu'))
    model.add(Dense(4,  activation='sigmoid'))
    model.compile(loss=weighted_mse(), optimizer='adam')
    return model
