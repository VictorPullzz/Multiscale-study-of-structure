import numpy as np

X = np.loadtxt('words.txt', dtype='str', delimiter=' - ')

mask = np.concatenate([np.random.choice(len(X), 16, replace=False) for i in range(int(26*3/16))])
print(len(mask))
print(X[mask])
