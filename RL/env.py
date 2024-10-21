import sys
import numpy as np

import gymnasium as gym
from ligand import Ligand
from protein import Protein
import plotly.express as px
from gymnasium import spaces
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import prepare_receptor4
import prepare_ligand4

p_path = r"/home/lachmansinghet/data1/RLMD/PDBbind_v2020_refined/refined-set/6fhq/6fhq_protein.pdb"
l_path = r"/home/lachmansinghet/data1/RLMD/PDBbind_v2020_refined/refined-set/6fhq/6fhq_ligand.mol2"


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
    
    def prepare_receptor(self, file_name):
        prepare_receptor4.main(file_name)
        return 
    
    def prepare_receptor(self, file_name):
        prepare_ligand4.main(file_name)
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
    
    def calculate_reward():

        return reward

    def step(self, action):
        
        reward = 1  # Example reward
        done = False  # Example terminal condition

        # 4th dimension in state space indicates the ligand with '1'
        # Apply action (only translation for now) to first three columns
        self.state[self.state[:,3] == 1, :3] += action

        # self.plot_3d_point_cloud_with_labels(self.state)

        return self.state, reward, done, {}, {}
    
    def plot_env(self):

        fig = px.scatter_3d(self.state, x=self.state[:,0], y=self.state[:,1], z=self.state[:,2], color=self.state[:,3])
        fig.update_traces(marker_size = 2)
        fig.show()

        return

    def plot_3d_point_cloud_with_labels(self, points):
        """
        Plots a 3D point cloud where each point has x, y, z coordinates and a 4th dimension for color labeling.
        
        Parameters:
        - points: A numpy array of shape (n, 4) where each row is [x, y, z, label].
        label should be either 0 or 1, and will determine the color of the point.
        """
        # Extract x, y, z coordinates and labels from the input array
        x_coords = points[:, 0]
        y_coords = points[:, 1]
        z_coords = points[:, 2]
        labels = points[:, 3]  # 0 or 1
        
        # Define colors for the labels: 0 -> 'red', 1 -> 'blue'
        colors = np.where(labels == 1, 'blue', 'red')
        
        # Create the 3D plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Scatter plot for the point cloud
        scatter = ax.scatter(x_coords, y_coords, z_coords, c=colors, marker='o', s=50, alpha=0.8)
        
        # Set plot labels and title
        ax.set_title('3D Point Cloud with Color Labels')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Show plot
        plt.show()

    def reset(self, options, seed=None):
        dict = {}
        return self.state, dict
    
    def render(self, mode='human'):
        # Render the environment (optional)
        print(f"State: {self.state}")

    def close(self):
        pass





