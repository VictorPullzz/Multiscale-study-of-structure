# Here we will add all experimental functions we use
# Some of them we may move to other files, if necessary
import re
import numpy as np

from glob import glob

def get_Xy(pos_spectra):
    files = glob(pos_spectra)
    X = []
    y = []
    pattern = re.compile(r'\d+')
    for file in files:
        data = np.loadtxt(file, skiprows=2)
        X.append(data[:,1])
        cns = np.asarray(pattern.findall(file), dtype=int)
        y.append(cns)
    E = data[:,0]
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y, E

def deformate(energy, XANES, alpha, shift):
    new_energy = energy * (1 + alpha) + shift
    return np.interp(new_energy, energy, XANES)

def extract_pos_of_cluster(clustfile):
    pattern = re.compile('[0-9_]+')
    with open(clustfile, 'r') as cl:
        cluster_positions = {}
        for line in cl:
            if pattern.match(line):
                pos = pattern.findall(line)
                if (len(pos) == 2):
                    cluster_positions[pos[0]] = int(pos[1])
    return cluster_positions
