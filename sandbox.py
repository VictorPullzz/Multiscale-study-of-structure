import numpy as np
import matplotlib.pyplot as plt
import os
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize


def load(f_name):
    ref = np.loadtxt(f_name, skiprows=1)
    E  = ref[:,0]
    mu = ref[:,1]

    dmu_dE = (mu[1:] - mu[:-1]) / (E[1:] - E[:-1])
    E0 = E[np.argmax(dmu_dE)]
    E = E - E0
    mask = (E > -20) & (E < 100)
    E = E[mask]
    mu = mu[mask]
    new_E  = np.arange(-20, 100)
    new_mu = np.interp(new_E, E, mu)
    new_mu -= new_mu.min()
    return np.array([new_E, new_mu / new_mu.max()]).T

def create_template(params):
    print(params)
    template = """
    Calculation
    Sim/Test_stand/Pt/Pt.txt
    Convolution
    EFermi            ! To change the Fermi level (or energy of the first non occupied state)
    %f

    Estart            ! To get the convoluted spectra starting at lower energy
    %f

    Gamma_max         ! To change the broadening width
    %f

    Gamma_hole
    %f

    Conv_out          ! To specify an output file name
    Sim/Test_stand/Pt/Pt_conv.txt

    End
    """ % tuple(params)
    with open('Sim/Test_stand/in/Pt_conv_inp.txt', 'w') as f:
        f.write(template)

np.random.seed(42)
os.chdir('3rd-party/fdmnes')
import subprocess

def objective(params):
    create_template(params)
    subprocess.call("./fdmnes_linux64")
    data_ref = load('../../Ref_Pt.txt')
    data     = load('Sim/Test_stand/Pt/Pt_conv.txt')
    #return np.sum(data[:,1] * data_ref[:,1])
    return np.mean((data[:,1] - data_ref[:,1]) ** 2)

res_gp = gp_minimize(objective, [(-7.,7.),(-10.,10.),(2.,15.),(0.,10.)], n_calls=100, n_random_starts=20, noise=1e-10, random_state=42, verbose=True)
create_template(res_gp.x)
subprocess.call("./fdmnes_linux64")

print("Best score=%.4f" % res_gp.fun)
print(res_gp.x)

data_ref = load('../../Ref_Pt.txt')
data     = load('Sim/Test_stand/Pt/Pt_conv.txt')

plt.subplot(121)
plt.plot(data_ref[:,0], data_ref[:,1])
plt.plot(data[:,0], data[:,1])
plt.subplot(122)
plt.plot(data_ref[:-1,0], data_ref[1:,1]-data_ref[:-1,1])
plt.plot(data[:-1,0], data[1:,1]-data[:-1,1])
plt.show()
