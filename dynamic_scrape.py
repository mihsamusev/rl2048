from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

class Interface2048:
    """Dynamic scraper for the game state
    We're looking for tile-container class that
    contains dynamic data of the board state
    since the site is dynamic we need to mimic being a 
    client / a browser that will execute the JavaScrip
    """
    MOVE_MAP ={
        0: Keys.LEFT,
        1: Keys.UP,
        2: Keys.RIGHT,
        3: Keys.DOWN
    }
    TILE_REGEX = re.compile(r"-(\d+)")
    WEBSITE = "https://play2048.co/"

    def __init__(self, driverpath, website=WEBSITE):
        self.driver = webdriver.Firefox(executable_path=driverpath)
        self.driver.get(website)
        self.prev_score = 0

    def close(self):
        self.driver.quit()

    def restart(self):
        self.prev_score = 0
        self.driver.find_element_by_class_name("restart-button").click()

    def game_over(self):
        """check if game is lost, return bool"""
        web_obj = self.driver.find_element_by_class_name("game-message")
        return web_obj.is_displayed()

    @staticmethod
    def _decode_tile(text):
        value, i, j = Interface2048.TILE_REGEX.findall(text)
        i = int(i) - 1
        j = int(j) - 1
        return int(value), i, j

    def get_state(self):
        web_obj = self.driver.find_elements_by_class_name("tile")
        state = 16 * [0]
        for w in web_obj:
            tile_str = w.get_attribute("class")
            value, i, j = Interface2048._decode_tile(tile_str)
            state[i * 4 + j] = value
        return state

    def get_score(self):
        web_obj = self.driver.find_element_by_class_name("score-container")
        score = re.findall(r"(\d+)", web_obj.text)
        return int(score[0])

    def get_reward(self):
        score = self.get_score()
        reward = score - self.prev_score
        self.prev_score = score
        return reward

    def move(self, idx):
        """Choose a move to send to the website as a key press
        [0 1 2 3] -> [Left Up Right Down]
        """
        key = Interface2048.MOVE_MAP[idx]
        self.driver.find_element_by_tag_name("body").send_keys(key)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "tile")))


if __name__ == "__main__":
    import random
    DRIVERPATH = "/home/msa/Documents/repos/rl2048/geckodriver"
    interface = Interface2048(DRIVERPATH)

    for i in range(2):
        interface.restart()
        while not interface.game_over():
            move_id = random.randint(0, 3)
            interface.move(move_id)
            state = interface.get_state()
            s = interface.get_score()
            r = interface.get_reward()
            print(r, s)
    interface.close()





