import time
import subprocess
import cv2
import random


import controller
import enviroment
import state

class Game:
    def __init__(self):
        self.controller = controller.Keyboard()
        self.state = state.State()
    

    def start(self):
        process = subprocess.Popen(enviroment.game_cmd, shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(3)
        self.setting()
        time.sleep(3)
        self.play()

    def setting(self):
        # difficulty : hard
        self.controller.press_command_c()
        self.controller.press_s()
        self.controller.press_h()

        # game target score : 5
        self.controller.press_command_c()
        self.controller.press_p()
        self.controller.press_a()

    def play(self):
        self.controller.press_enter()
        time.sleep(0.5)
        self.controller.press_enter()
        time.sleep(0.5)
        self.controller.press_enter()

    def reset(self):
        self.state = state.State()
        self.play()

    def random_press(self):
        action = random.randint(1,10)
        if action == 1:
            self.controller.up()
        elif action == 2:
            self.controller.left()
        elif action == 3:
            self.controller.right()
        elif action == 4:
            self.controller.up_attack()
        elif action == 5:
            self.controller.down_attack()
        elif action == 6:
            self.controller.left_attack()
        elif action == 7:
            self.controller.right_attack()
        elif action == 8:
            self.controller.up_left_attack()
        elif action == 9:
            self.controller.up_right_attack()
        elif action == 10:
            self.controller.up_empty_attack()

    
        


