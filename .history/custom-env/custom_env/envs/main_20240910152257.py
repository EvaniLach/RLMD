import gymnasium as gym
import custom_env
from env import Environment


if __name__ == "__main__":
    env = Environment()
    env.plot_env()
    # env = gym.make('c_env')
