import gym
import gym_wumpus
env = gym.make('wumpus-extra-v0')

for i_episode in range(20000):
    observation = env.reset()
    print(observation)
    for t in range(100):
        #env.render()
        #print("Observstion:", observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if i_episode > 19800 and done:
            print("Final Score:", env.getScore())
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()