# Here we will add all experimental functions we use
# Some of them we may move to other files, if necessary
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
