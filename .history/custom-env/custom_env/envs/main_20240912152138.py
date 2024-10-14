import gymnasium as gym
import custom_env
from env import Environment
from a2c import Agent

p_path = r"C:\\Users\\evani\\OneDrive\\Documenten\\Phd\\RLMD\\PDBbind_v2020_refined\\refined-set\\6fhq\\6fhq_protein.pdb"
l_path = r"C:\Users\evani\OneDrive\Documenten\Phd\RLMD\PDBbind_v2020_refined\refined-set\6fhq\6fhq_ligand.mol2"


iterations = 1

if __name__ == "__main__":
    env = Environment(p_path, l_path)
    agent = Agent()

    for i in range(iterations):
        env.reset()
        state = env.combine_states()
        action, logprob, _, value = agent.get_action_and_value(state)
        print(action)
        next_obs, reward, terminations, truncations, infos = env.step(action.cpu().numpy())




    # env = gym.make('c_env')
