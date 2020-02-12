from gym.envs.registration import register

register(
    id='wumpus-v0',
    entry_point='gym_wumpus.envs:WumpusEnv',
)
register(
    id='wumpus-extra-v0',
    entry_point='gym_wumpus.envs:WumpusExtraEnv',
)
