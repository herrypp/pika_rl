import cv2
import pyscreenshot
import numpy as np

import enviroment

class State:
    def __init__(self):
        self.screen = None
        self.left_score = 0
        self.right_score = 0
        self.is_game_set = False
        self.is_score_set = False
        self.dark_screen_time = 0

    def update(self):
        self.update_screen()
        self.update_score()
        self.update_set()

    def update_screen(self):
        # screenshot the pikaball window
        pil_image = pyscreenshot.grab(bbox=(enviroment.screen_left, enviroment.screen_top,
         enviroment.screen_right, enviroment.screen_bottom))
        np_image = np.asarray(pil_image)
        # We just concern about pikachu & ball
        filter_image = self.img_filtering(np_image)
        cv2_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)

        self.screen = cv2_image

    def update_score(self):
        left_score_img = self.screen[19:77, 94:147]
        right_score_img = self.screen[19:77, 774:827]

        new_score = self.get_score(left_score_img)
        if new_score != -1:
        	self.left_score = new_score

        new_score = self.get_score(right_score_img)
        if new_score != -1:
        	self.right_score = new_score

    def update_set(self):
    	self.is_game_set = False
    	self.is_score_set = False

    	is_dark = sum(sum(self.screen)) == 0

    	if is_dark:
    		# continuous dark -> game set
    		if self.dark_screen_time != 0:
    			self.is_game_set = True
    		self.dark_screen_time = self.dark_screen_time + 1
    	else:
    		# dark only show once -> score set
    		if self.dark_screen_time != 0:
    			self.is_score_set = True
    		self.dark_screen_time = 0

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
