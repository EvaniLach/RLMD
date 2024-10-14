from gymnasium.envs.registration import register

register(
    id='c_env',
    entry_point='custom_env.envs:Environment',
)