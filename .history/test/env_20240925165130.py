import gymnasium as gym
from gymnasium import spaces
import numpy as np
from protein import Protein
from ligand import Ligand
import plotly.express as px

p_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_protein.pdb"
l_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_ligand.mol2"



class Environment(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode=None, size=5):
        super(Environment, self).__init__()

        # Create state from protein and ligand files
        self.state = self.create_state()
        # Get shape to instantiate observation space
        obs_shape = self.state.shape
        
        # Observation space 
        self.observation_space = spaces.Box(low=0, high=100, shape=obs_shape, dtype=np.float32)

        # Action space
        # For now, we only do translation
        self.action_space = spaces.Box(low=-10, high=10, shape=(3,), dtype=np.float32)

        return
    
    def create_state(self):
        # Create Protein() using file
        protein = Protein(p_path)
        self.state_p = protein.retrieve_coords()

        # Create Ligand() using file
        ligand = Ligand(l_path)
        self.state_l = ligand.retrieve_coords()

        # Combine P & L state into one
        state = np.concatenate((self.state_p, self.state_l))

        return state

    def step(self, action):
        
        reward = 1  # Example reward
        done = False  # Example terminal condition

        # 4th dimension in state space indicates the ligand with '1'
        # Apply action (only translation for now) to first three columns
        self.state[self.state[:,3] == 1, :3] += action

        return self.state, reward, done, {}, {}
    
    def plot_env(self):

        state = self.combine_states()
        fig = px.scatter_3d(state, x=state[:,0], y=state[:,1], z=state[:,2], color=state[:,3])
        fig.update_traces(marker_size = 2)
        fig.show()

        return


    def reset(self, options, seed=None):
        dict = {}
        return self.state, dict
    
    def render(self, mode='human'):
        # Render the environment (optional)
        print(f"State: {self.state}")


    def close(self):
        pass





