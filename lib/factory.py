import numpy as np
import os
import subprocess

from ase.neighborlist import NeighborList
from ase.cluster.cubic import FaceCenteredCubic
from ase.visualize import view
from ase.atoms import Atoms
from ase.io import write


class ClustersFactory():
    def __init__(self, atomtype, range_lim, latticetype = 'fcc',
    surfaces=[(1, 0, 0), (1, 1, 0), (1, 1, 1)]):
        self.atomtype = atomtype
        self.latticetype = latticetype
        self.surfaces = surfaces
        self.lc = self.get_lc()
        self.range_lim = range_lim

    def get_lc(self):
        """Getting lattice constant value"""
        if self.atomtype == 'Pt':
            lc = 3.92420
        elif self.atomtype == 'Cu':
            lc = 3.61490
        return lc

    def get_unique_pos(self, atoms):
        """Returns CNs as np.array, list of indices of atoms for every position
        and list with counts of the positions"""
        lc_2 = self.lc / 2 ** 0.5
        nls = [NeigbourListFactory(R, atoms) for R in [lc_2, self.lc, lc_2 * 3 ** 0.5, lc_2 * 2]]
        spheres = {'s1': [], 's2': [], 's3': [], 's4': []}
        for a in atoms:
            s = 0
            for i, nl in enumerate(nls):
                indices, _ = nl.get_neighbors(a.index)
                spheres['s' + str(i+1)].append(len(indices) - s)
                s += len(indices) - s
        CNs = np.array([spheres[key] for key in sorted(spheres.keys())]).T
        CNs, u_ind, counts =  np.unique(CNs, axis=0, return_counts=True, return_index=True)
        return CNs, u_ind, counts

    def neighborlist_factory(R, atoms):
    '''Возвращает объект класса NeighborList, в котором содержится список
    соседей в пределах сферы радиуса R для объекта atoms.
    Получить список соседей - метод get_neighbors(номер атома)
    self_interaction - считает ли атом самого себя соседом
    bothways=True - возвращает всех соседей (False - только половина)'''
        nl = NeighborList([R * 0.5 + 0.01] * len(atoms), self_interaction=False, bothways=True)
        nl.update(atoms)
        return nl

    def change_zero(atoms, c_coords):
    """Returns coordinates minus coodinates of the central atoms
    so we translate zero to the central atom. c_coords - coords of central atom"""
        z = np.zeros((len(atoms), 3))
        for i in range(len(atoms)):
            z[i] = c_coords
        atoms.set_positions(atoms.get_positions() - z)
        return atoms

    # def generate_clusters(self, folder, max_size=200):
    #     """Generating clusters with ASE library and writing .xyz files
    #     of clusters coordinates"""
    #     num = 0
    #     for i in range(-lim_of_range, lim_of_range):
    #         for j in range(-lim_of_range, lim_of_range):
    #             for k in range(-lim_of_range, lim_of_range):
    #                 layers = [i, j, k]
    #                 if self.latticetype == 'fcc':
    #                     atoms = FaceCenteredCubic(atomtype, surfaces, layers,
    #                     latticeconstant=self.lc)
    #                 if len(atoms) > max_size:
    #                     continue
    #                 atoms = Atoms(atoms)
    #                 cluster_name = str(len(atoms)) + '_' + str(num) + '.xyz'
    #                 if os.path.exists('data'+ folder + '/clusters_coordinates/' + cluster_name):
    #                     continue
    #                 else:
    #                     write('/data/' + folder + '/clusters_coordinates/' + cluster_name, atoms)
    #                 nl = neighborlist_factory(self.lc*2**0.5, atoms)
    #                 for CN, u_ind, count in zip(*get_unique_pos(atoms, self.lc)):
    #                     change_zero(atoms, atoms.get_positions()[u_ind])
    #                     position_name = _'.join(map(str, CN)) + '.xyz'
    #                     #Bad code below
    #                     if os.path.exists('/data/' + folder + '/positions_coordinates/' + position_name):
    #                         continue
    #                     else:
    #                         write('/data/' + folder + '/positions_coordinates/' + position_name +
    #                         atoms[np.append([u_ind], nl.get_neighbors(u_ind)[0])])
    #                         f = open('/data/' + folder + '/positions_count/' + cluster_name, 'a')
    #                         f.write('_'.join(map(str, CN))+ ' ' + str(count) +'\n') #пишем, из каких неэквивал. позиций состоит кластер и сколько их в кластере
    #                         f.close()
    #
    #                 num += 1

cf = ClustersFactory('Cu', 10)
cf.generate_clusters('Cu', 3)
