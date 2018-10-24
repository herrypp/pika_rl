import cv2
import pyscreenshot
import numpy as np
import time
import threading

import enviroment

class State:
    def __init__(self):
        self.screen = None
        self.resize_screen = None
        self.left_score = 0
        self.right_score = 0
        self.is_episode_start = False
        self.is_step_start = False
        self.is_score_change = False

    def update(self):
        self.update_screen()
        self.update_score()

    def update_screen(self):
        # screenshot the pikaball window
        pil_image = pyscreenshot.grab(bbox=(enviroment.screen_left, enviroment.screen_top,
         enviroment.screen_right, enviroment.screen_bottom))
        np_image = np.asarray(pil_image)
        # We just concern about pikachu & ball
        filter_image = self.img_filtering(np_image)
        cv2_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)

        self.screen = cv2_image
        self.resize_screen = cv2.resize(cv2_image, (enviroment.input_height, enviroment.input_width))

    def update_score(self):
        self.is_score_change = False
        left_score_img = self.screen[19:77, 94:147]
        right_score_img = self.screen[19:77, 774:827]

        new_score = self.get_score(left_score_img)
        if new_score != -1 and self.left_score != new_score:
            self.left_score = new_score
            self.is_score_change = True
            if new_score == 5:
                self.is_episode_start = True
            else:
                thread = threading.Thread(target=self.set_step_start, args=())
                thread.daemon = True
                thread.start()

        new_score = self.get_score(right_score_img)
        if new_score != -1 and self.right_score != new_score:
            self.right_score = new_score
            self.is_score_change = True
            if new_score == 5:
                self.is_episode_start = True
            else:
                thread = threading.Thread(target=self.set_step_start, args=())
                thread.daemon = True
                thread.start()

    def check_episode_start(self):
        if self.is_episode_start:
            self.is_episode_start = False
            return True
        else:
            return False

    def set_step_start(self):
        time.sleep(2)
        self.is_step_start = True

    def check_step_start(self):
        if self.is_step_start:
            self.is_step_start = False
            return True
        else:
            return False


    def img_filtering(self, img):
        img_filterd = img.copy()
        # remove pixels containing heavy blue or light red
        img_filterd[img[:,:,2] > 127] = [0, 0, 0, 255]
        img_filterd[img[:,:,0] < 160] = [0, 0, 0, 255]

        return img_filterd


    def get_score(self, score_img):
        if np.array_equal(score_img, enviroment.number_image[0]):
            return 0
        elif np.array_equal(score_img, enviroment.number_image[1]):
            return 1
        elif np.array_equal(score_img, enviroment.number_image[2]):
            return 2
        elif np.array_equal(score_img, enviroment.number_image[3]):
            return 3
        elif np.array_equal(score_img, enviroment.number_image[4]):
            return 4
        elif np.array_equal(score_img, enviroment.number_image[5]):
            return 5
        else:
            return -1
