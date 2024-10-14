import pandas as pd
from biopandas.pdb import PandasPdb
from typing import Optional
import pdbreader
import numpy as np

import plotly.express as px



path = r"C:\\Users\\evani\\OneDrive\\Documenten\\Phd\\RLMD\\PDBbind_v2020_refined\\refined-set\\6fhq\\6fhq_protein.pdb"

class Protein():
    def __init__(self, path):

        dict = pdbreader.read_pdb(path)
        self.df = pd.concat((dict["ATOM"], dict["HETATM"]))

    def retrieve_coords(self):
        np.array(())
        return self.df.x, self.df.y, self.df.z

