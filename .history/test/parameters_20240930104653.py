import pandas as pd
import numpy as np

class Params():

    def __init__(self):

        # Atom parameters taken from most recent AutoDock Vina code: https://github.com/ccsb-scripps/AutoDock-Vina/blob/develop/data/AD4_parameters.dat

        # - Atom Types
        # - Rii = sum of vdW radii of two like atoms (in Angstrom)
        # - epsii = vdW well depth (in Kcal/mol)
        # - vol = atomic solvation volume (in Angstrom^3)
        # - solpar = atomic solvation parameter
        # - Rij_hb = H-bond radius of the heteroatom in contact with a hydrogen (in Angstrom)
        # - epsij_hb = well depth of H-bond (in Kcal/mol)
        # - hbond = integer indicating type of H-bonding atom (0=no H-bond)
        # - rec_index = initialised to -1, but later on holds count of how many of this atom type are in receptor
        # - map_index = initialised to -1, but later on holds the index of the AutoGrid map
        # - bond_index = used in AutoDock to detect bonds; see "mdist.h", enum {C,N,O,H,XX,P,S}

        self.atom_params = pd.DataFrame(
            columns = ["atom_type", "Rii", "epsii", "vol", "solpar", "rij_hb", "epsij_hb", "hbond", "rec_index", "map_index", "bond_index", "elemet"],
            data = [['H', 2.0, 0.02, 0.0, 0.00051, 0.0, 0.0, 0, -1, -1, 3, 'H'],
                    ['HD', 2.0, 0.02, 0.0, 0.00051, 0.0, 0.0, 2, -1, -1, 3, 'H'],
                    ['HS', 2.0, 0.02, 0.0, 0.00051, 0.0, 0.0, 1, -1, -1, 3, 'H'],
                    ['C', 4.0, 0.15, 33.5103, -0.00143, 0.0, 0.0, 0, -1, -1, 0, 'C'],
                    ['A', 4.0, 0.15, 33.5103, -0.00052, 0.0, 0.0, 0, -1, -1, 0, 'C'],
                    ['N', 3.5, 0.16, 22.4493, -0.00162, 0.0, 0.0, 0, -1, -1, 1, 'N'],
                    ['NA', 3.5, 0.16, 22.4493, -0.00162, 1.9, 5.0, 4, -1, -1, 1, 'N'],
                    ['NS', 3.5, 0.16, 22.4493, -0.00162, 1.9, 5.0, 3, -1, -1, 1, 'N'],
                    ['OA', 3.2, 0.2, 17.1573, -0.00251, 1.9, 5.0, 5, -1, -1, 2, 'O'],
                    ['OS', 3.2, 0.2, 17.1573, -0.00251, 1.9, 5.0, 3, -1, -1, 2, 'O'],
                    ['F', 3.09, 0.08, 15.448, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'F'],
                    ['Mg', 1.3, 0.875, 1.56, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Mg'],
                    ['MG', 1.3, 0.875, 1.56, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Mg'],
                    ['P', 4.2, 0.2, 38.7924, -0.0011, 0.0, 0.0, 0, -1, -1, 5, 'P'],
                    ['SA', 4.0, 0.2, 33.5103, -0.00214, 2.5, 1.0, 5, -1, -1, 6, 'S'],
                    ['S', 4.0, 0.2, 33.5103, -0.00214, 0.0, 0.0, 0, -1, -1, 6, 'S'],
                    ['Cl', 4.09, 0.276, 35.8235, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Cl'],
                    ['CL', 4.09, 0.276, 35.8235, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Cl'],
                    ['Ca', 1.98, 0.55, 2.77, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Ca'],
                    ['CA', 1.98, 0.55, 2.77, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Ca'],
                    ['Mn', 1.3, 0.875, 2.14, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Mn'],
                    ['MN', 1.3, 0.875, 2.14, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Mn'],
                    ['Fe', 1.3, 0.01, 1.84, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Fe'],
                    ['FE', 1.3, 0.01, 1.84, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Fe'],
                    ['Zn', 1.48, 0.55, 1.7, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Zn'],
                    ['ZN', 1.48, 0.55, 1.7, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Zn'],
                    ['Br', 4.33, 0.389, 42.5661, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Br'],
                    ['BR', 4.33, 0.389, 42.5661, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'Br'],
                    ['I', 4.72, 0.55, 55.0585, -0.0011, 0.0, 0.0, 0, -1, -1, 4, 'I'],
                    ['Z', 4.0, 0.15, 33.5103, -0.00143, 0.0, 0.0, 0, -1, -1, 0, 'D'],
                    ['G', 4.0, 0.15, 33.5103, -0.00143, 0.0, 0.0, 0, -1, -1, 0, 'D'],
                    ['GA', 4.0, 0.15, 33.5103, -0.00052, 0.0, 0.0, 0, -1, -1, 0, 'D'],
                    ['J', 4.0, 0.15, 33.5103, -0.00143, 0.0, 0.0, 0, -1, -1, 0, 'D'],
                    ['Q', 4.0, 0.15, 33.5103, -0.00143, 0.0, 0.0, 0, -1, -1, 0, 'D'],
                    ['W', 0.0, 0.2, 0.0, -0.0, 0.0, 0.0, 0, -1, -1, 2, 'O']]
        )





