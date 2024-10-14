import gymnasium as gym
import custom_env

if __name__ == "__main__":
    env = gym.make('c_env')
    env.plot_env()