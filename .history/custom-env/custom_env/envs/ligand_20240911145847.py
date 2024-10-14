import pandas as pd
from biopandas.pdb import PandasPdb
from typing import Optional
import pdbreader
import numpy as np
from moldf import read_mol2 

path = r"C:\\Users\\evani\\OneDrive\\Documenten\\Phd\\RLMD\\PDBbind_v2020_refined\\refined-set\\6fhq\\6fhq_ligand.mol2"
translation_vector = np.array([2,2,2])

class Ligand():
    def __init__(self, path):

        dict = read_mol2(path)
        self.df = dict["ATOM"]
        self.df["type"] = self.df["atom_name"].str.slice(0, 1)
        self.coords = self.retrieve_coords(self.df)

        return

    def retrieve_coords(self):
        coords = self.df[["x", "y", "z"]].to_numpy()
        # Annotate x,y,z values with 1 to indicate ligand
        ann = np.ones((len(coords),1))
        coords = np.hstack((coords, ann))
        return coords

    def translate(self):
        self.coords = self.coords + translation_vector

        return


