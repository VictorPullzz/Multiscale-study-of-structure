import numpy as np
import keras
from utils import deformate

class MyGenerator(keras.utils.Sequence):
    def __init__(self, E, X, y, Nmin, Nmax, dE, dA, batch_size=32, mode='random'):
        assert len(X) == len(y), "Length missmatch!"
        assert len(E) == X.shape[-1], "Length missmatch!"
        self.E = E
        self.X = X
        self.y = y
        self.Nmin = Nmin
        self.Nmax = Nmax
        self.dE = dE
        self.dA = dA
        self.batch_size = batch_size
        self.mode = mode
        self.on_epoch_end()

    def __len__(self):
        return 1

    def __getitem__(self, ind):
        if self.mode == 'random':
            return self.get_random(ind)
        if self.mode == 'variant1':
            return self.get_variant1(ind)

    def get_random(self, ind):
        result_X = np.zeros((self.batch_size, len(self.E)))
        result_y = np.zeros((self.batch_size, 4)) #<------------------------------------- hardcoded!
        for i in range(self.batch_size):
            size = np.random.randint(self.Nmin, self.Nmax)
            mask = np.random.choice(len(self.X), size=size, replace=False)
            weights = np.random.rand(len(mask))
            weights /= weights.sum()
            weights = sorted(weights, reverse=True)

            for j, w in zip(mask, weights):
                X = deformate(self.E, self.X[j], np.random.randn()*self.dA, np.random.randn()*self.dE)
                result_X[i] += X * w
                result_y[i] += self.y[j] * w
        result_X /= np.max(result_X, axis=-1)[:, None]
        result_X = result_X[:,1:] - result_X[:,:-1]
        return result_X, result_y / np.array([12,6,24,12])

    def get_variant1(self, ind):
        result_X = np.zeros((self.batch_size, len(self.E)))
        result_y = np.zeros((self.batch_size, 4)) #<------------------------------------- hardcoded!
        for i in range(self.batch_size):
            size = np.random.randint(self.Nmin, self.Nmax)
            mask = np.random.choice(len(self.X), size=size, replace=False)
            weights = np.random.rand(size)
            weights /= weights.sum()
            indices = np.argsort(self.y[mask,0])[::-1]
            mask = mask[indices]
            alpha = np.random.randn(size) * self.dA
            alpha = np.sort(alpha)
            for a, j, w in zip(alpha, mask, weights):
                X = deformate(self.E, self.X[j], a, np.random.randn()*self.dE)
                result_X[i] += X * w
                result_y[i] += self.y[j] * w
        result_X /= np.max(result_X, axis=-1)[:, None]
        result_X = result_X[:,1:] - result_X[:,:-1]
        return result_X, result_y / np.array([12,6,24,12])

    def on_epoch_end(self):
        pass

class DataAugmentator(keras.utils.Sequence):
    def __init__(self, X, y):
        self.X = X
        self.y = y
