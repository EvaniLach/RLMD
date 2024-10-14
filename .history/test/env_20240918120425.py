import gymnasium as gym
from gymnasium import spaces
import numpy as np
from protein import Protein
from ligand import Ligand
import plotly.express as px



class Environment(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode=None, size=5):
        super(Environment, self).__init__()
        
        # Observation space 
        self.observation_space = spaces.Box(low=0, high=100, shape=(100,3), dtype=np.float32)

        # # Observation space 
        # self.observation_space = spaces.Dict(
        #     {
        #         "protein": spaces.Box(low=0, high=100, shape=(100,3), dtype=np.float32),
        #         "ligand": spaces.Box(low=0, high=100, shape=(100,3), dtype=np.float32)
        #     }
        # )

        # Action space 
        self.action_space = spaces.Box(low=-10, high=10, shape=(2, 3), dtype=np.float32)

        self.p_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_protein.pdb"
        self.l_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_ligand.mol2"

        return
    
    def combine_states(self):
        state = np.concatenate((self.state_p, self.state_l))
        return state

    def step(self, action):
        
        reward = 1  # Example reward
        done = False  # Example terminal condition

        self.model()

        return self.state, reward, done, {}
    
    def plot_env(self):

        state = self.combine_states()
        fig = px.scatter_3d(state, x=state[:,0], y=state[:,1], z=state[:,2], color=state[:,3])
        fig.update_traces(marker_size = 2)
        fig.show()
        return

    def reset(self, options, seed=None):
        protein = Protein(self.p_path)
        self.state_p = protein.retrieve_coords()

        ligand = Ligand(self.l_path)
        self.state_l = ligand.retrieve_coords()

        state = self.combine_states()
        print("state shape", state.shape)
        dict = {}

        return state, dict
    
    def render(self, mode='human'):
        # Render the environment (optional)
        print(f"State: {self.state}")


    def close(self):
        pass





