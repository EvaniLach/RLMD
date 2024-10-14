import pandas as pd

class Params():

    def __init__(self):
        self.atom_params = pd.DataFrame(
            columns = ["atom_type", "Rii", "epsii", "vol", "solpar", "rij_hb", "epsij_hb", "hbond", "rec_index", "map_index", "bond_index", "elemet"],
            data=[[2.00,  0.020,   0.0000 ,  0.00051,  0.0,  0.0,  0,  -1,  -1,  3]]  
        )


