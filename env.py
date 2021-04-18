from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

class Env2048(Env):
    def __init__(self, game_interface):
        self.action_space = Discrete(4)
        self.observation_space = Box(
            0, 15, (4, 4), dtype=np.uint32)
        
        # interface with selenium
        self.game_interface = game_interface
        self.game_interface.restart()

    def reset(self):
        self.game_interface.restart()
        return self.game_interface.get_state()

    def step(self, action):
        ""
        self.game_interface.move(action)
        
        state = self.game_interface.get_state()
        done = self.game_interface.game_over()
        if done:
            reward = - 500
        else:
            reward = self.game_interface.get_reward()
        info = ""
        return state, reward, done, info

    def close(self):
        self.game_interface.close()
