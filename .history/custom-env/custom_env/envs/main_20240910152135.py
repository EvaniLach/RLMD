import gymnasium as gym
import custom_env
import envs.env


if __name__ == "__main__":
    env = envs.env()
    env.plot_env()
    # env = gym.make('c_env')
