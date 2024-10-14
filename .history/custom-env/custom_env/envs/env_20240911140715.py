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
        self.observation_space = spaces.Dict(
            {
                "protein": spaces.Box(low=0, high=100, shape=(100,3), dtype=np.float32),
                "ligand": spaces.Box(low=0, high=100, shape=(100,3), dtype=np.float32)
            }
        )


        # Action space 
        self.action_space = spaces.Dict(
            {
                "translation": spaces.Box(low=np.array([-1.0, -1.0, -1.0]), 
                                       high=np.array([1.0, 1.0, 1.0]), 
                                       dtype=np.float32),
                "rotation": spaces.Box(low=np.array([-1.0, -1.0, -1.0]), 
                                       high=np.array([1.0, 1.0, 1.0]), 
                                       dtype=np.float32)
            }
        )

        return
    
    def initial_state(self):
        self.protein = Protein()
        self.state_p = self.protein.retrieve_coords()

        self.ligand = Ligand()
        self.state_l = self.ligand.retrieve_coords()

        return

    def step(self, action):
        
        reward = 1  # Example reward
        done = False  # Example terminal condition
        return self.state, reward, done, {}
    
    def plot_env(self, df):
    
        fig = px.scatter_3d(df, x='x', y='y', z='z', color='element')
        fig.update_traces(marker_size = 2)

        fig.show()


    def reset(self, path):
        self.state = np.zeros(3)
        return self.state

    def render(self, mode='human'):
        # Render the environment (optional)
        print(f"State: {self.state}")


    def close(self):
        pass





