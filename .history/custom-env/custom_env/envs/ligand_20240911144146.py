import pandas as pd
from biopandas.pdb import PandasPdb
from typing import Optional
import pdbreader
import numpy as np
from moldf import read_mol2 

path = r"C:\\Users\\evani\\OneDrive\\Documenten\\Phd\\RLMD\\PDBbind_v2020_refined\\refined-set\\6fhq\\6fhq_ligand.mol2"

class Ligand():
    def __init__(self, path):

        dict = read_mol2(path)
        self.df = dict["ATOM"]
        self.df["type"] = self.df["atom_name"].str.slice(0, 1)

        return

    def retrieve_coords(df):
        coords = df[["x", "y", "z"]].to_numpy()
        return coords

