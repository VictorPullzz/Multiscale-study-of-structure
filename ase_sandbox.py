import ase
from ase.spacegroup import crystal
from ase.visualize import view
from ase.lattice.cubic import FaceCenteredCubic
from ase.cluster.cubic import FaceCenteredCubic
from ase.cluster import Icosahedron
from ase.cluster import Cluster
from ase import Atoms
import numpy as np
from ase.cluster import Octahedron
from ase.cluster import Hexagonal
from ase.cluster import Decahedron
from lib.utils import get_gyration_radius


# def find_center(xyz_arr):
#     return sum(xyz_arr)/len(xyz_arr)
#
# def get_gyration_radius(xyz_arr):
#     center = find_center(xyz_arr)
#     res = np.round(xyz_arr - center, 8)
#     sq_sum = sum(sum(res**2))
#     radius = np.round(np.sqrt(sq_sum/len(xyz_arr)), 2)
#     return radius


surfaces = [(1, 0, 0), (1, 1, 1), (1, 1, 1)]
layers = [20, 20, 20]
atoms = FaceCenteredCubic('Pt', surfaces, layers)
print(len(atoms))
print('Radius of spherical particle with the same volume:', np.round(atoms.get_diameter(method='volume')/2, 2))
print('Average radius of three particle\'s directions:', np.round(atoms.get_diameter(method='shape')/2, 2))
print('Radius of gyration:', get_gyration_radius(atoms.get_positions()))
print('Radius of gyration * 5/4:', np.round(get_gyration_radius(atoms.get_positions())*5/4, 2))
print('**********************************************************************')

# method = 'volume': Returns the diameter of a sphere with the
# same volume as the atoms. (Default)

# method = 'shape': Returns the averaged diameter calculated from the
# directions given by the defined surfaces.

# print(len(atoms))

# view(atoms)

ico = Icosahedron('Pt', 2)

print(len(ico))
# view(ico)

octah = Octahedron('Pt', 4)
print(len(octah))
# view(octah)

# octahedron
# Type                            Condition
# ----                            ---------
# Regular octahedron              cutoff = 0
# Regular truncated octahedron    length = 3 * cutoff + 1
# Cuboctahedron                   length = 2 * cutoff + 1

# cuboctahedron:
cuboctah = Octahedron('Pt', cutoff=2, length=5)
print(len(cuboctah))
# view(cuboctah)

dec = Decahedron('Pt', p=3, q=3, r=1)
print(len(dec))
# view(dec)




# xyz_arr = dec.get_positions()
# print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# center = find_center(xyz_arr)
# print(center)
# res = np.round(xyz_arr - center, 8)
# print('Массив разностей:', res)
# res_sq = res**2
# print('Массив квадратов разностей:', res_sq)
#
# el_sum = 0
# for i in range(len(xyz_arr)):
#     el_sum += sum(res_sq[i])
#     print('Очередная строка:', sum(res_sq[i]))
#
# print(el_sum)
#
# sq_sum = sum(sum(res**2))
# print(sq_sum)
# radius = np.round(np.sqrt(sq_sum/len(xyz_arr)), 2)
# print(radius)
