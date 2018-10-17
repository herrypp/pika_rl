import time
import subprocess
import pyscreenshot
import cv2
import numpy as np

import controller
import enviroment

class Game:
    def __init__(self):
        self.controller = controller.Keyboard()

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

    def get_screen(self):
        # screenshot the pikaball window
        pil_image = pyscreenshot.grab(bbox=(enviroment.screen_left, enviroment.screen_top,
         enviroment.screen_right, enviroment.screen_bottom))
        np_image = np.asarray(pil_image)
        # We just concern about pikachu & ball
        filter_image = self.img_filtering(np_image)
        
        cv2_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)
        cv2_image = cv2.resize(cv2_image, (enviroment.input_width, enviroment.input_height))
        cv2.imwrite('test.png', cv2_image)

        return cv2_image

    def img_filtering(self, img):
        img_filterd = img.copy()
        # remove pixels containing heavy blue or light red
        img_filterd[img[:,:,2] > 127] = [0, 0, 0, 255]
        img_filterd[img[:,:,0] < 160] = [0, 0, 0, 255]

        return img_filterd

