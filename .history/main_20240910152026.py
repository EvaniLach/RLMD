import custom_env.envs
import gymnasium as gym
import custom_env

if __name__ == "__main__":
    env = custom_env.envs.Environment()
    env.plot_env()
    # env = gym.make('c_env')
