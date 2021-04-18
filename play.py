from env import Env2048
from dynamic_scrape import Interface2048

DRIVERPATH = "/home/msa/Documents/repos/rl2048/geckodriver"
interface = Interface2048(DRIVERPATH)
environment = Env2048(game_interface=interface)

for i_episode in range(20):
    observation = environment.reset()
    for t in range(100):
        print(observation)
        action = environment.action_space.sample()
        observation, reward, done, info = environment.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
environment.close()