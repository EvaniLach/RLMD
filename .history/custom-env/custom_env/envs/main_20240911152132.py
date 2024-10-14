import gymnasium as gym
import custom_env
from env import Environment

p_path = r"C:\\Users\\evani\\OneDrive\\Documenten\\Phd\\RLMD\\PDBbind_v2020_refined\\refined-set\\6fhq\\6fhq_protein.pdb"
l_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_ligand.mol2"


if __name__ == "__main__":
    env = Environment(p_path, l_path)
    env.reset()
    env.combine_states()
    env.plot_env()


    # env = gym.make('c_env')
