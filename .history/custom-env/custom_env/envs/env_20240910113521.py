import gymnasium as gym
from gymnasium import spaces
import numpy as np


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


    def step(self, action):
        # Execute one time step
        self.state = np.random.random(3)  # Random next state
        reward = 1  # Example reward
        done = False  # Example terminal condition
        return self.state, reward, done, {}

    def reset(self, path):
        # Reset environment to the initial state
        self.state_p = self.get_xyz(self.parse_pdb(path))
        self.state_l = self.get_xyz(self.parse_pdb(path))


        self.state = np.zeros(3)
        return self.state

    def render(self, mode='human'):
        # Render the environment (optional)
        print(f"State: {self.state}")

    def parse_pdb(self, file_path):
        atoms = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(('ATOM', 'HETATM')):
                    atom = {
                        'atom_name': line[12:16].strip(),
                        'residue_name': line[17:20].strip(),
                        'chain_id': line[21].strip(),
                        'residue_seq': int(line[22:26].strip()),
                        'x': float(line[30:38].strip()),
                        'y': float(line[38:46].strip()),
                        'z': float(line[46:54].strip()),
                        'element': line[76:78].strip()
                    }
                    atoms.append(atom)
            
        return np.array(atoms)
    
    def get_xyz(self, file):
        x_list = []
        y_list = []
        z_list = []

        for i in range(len(file)):
            x_list.append(file[i]["x"])
            y_list.append(file[i]["y"])
            z_list.append(file[i]["z"])
        
        return np.column_stack((x_list, y_list, z_list))

    def close(self):
        pass





