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
        self.input = None
        self.reward = 0
        self.crash = False
        self.white_image_time = 0

    def update(self):
        self.update_screen()
        self.update_score()
        self.update_input()

    def update_screen(self):
        # screenshot the pikaball window
        pil_image = pyscreenshot.grab(bbox=(enviroment.screen_left, enviroment.screen_top,
         enviroment.screen_right, enviroment.screen_bottom))
        np_image = np.asarray(pil_image)
        self.crash_detect(np_image)
        # We just concern about pikachu & ball
        filter_image = self.img_filtering(np_image)
        # cv2.imshow('resize image', cv2.resize(filter_image, (enviroment.input_height, enviroment.input_width)))
        # cv2.waitKey(1)
        cv2_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)

        self.screen = cv2_image
        self.resize_screen = cv2.resize(cv2_image, (enviroment.input_width, enviroment.input_height))
        

    def update_score(self):
        self.is_score_change = False
        self.reward = 1
        left_score_img = self.screen[19:77, 94:147]
        right_score_img = self.screen[19:77, 774:827]

        new_score = self.get_score(left_score_img)
        if new_score != -1 and self.left_score != new_score:
            self.left_score = new_score
            self.is_score_change = True
            self.reward = -100
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
            self.reward = 100
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

    def update_input(self):
        object_list = []
        object_list.extend(self.find_object(Object.Left_pika))
        object_list.extend(self.find_object(Object.Right_pika))
        object_list.extend(self.find_object(Object.Ball))
        
        self.input = np.asarray(object_list).reshape(1, -1)

    def find_object(self, obj):
        start = 0
        end = 0
        light = 0
        size_x = 0
        size_y = 0
        if obj == Object.Left_pika:
            start = 0
            end = int(enviroment.input_width/2)
            light = 232
            size_y = 1
            size_x = 12
        elif obj == Object.Right_pika:
            start = int(enviroment.input_width/2)
            end = enviroment.input_width
            light = 232
            size_y = 1
            size_x = 12
        else:
            start = 0
            end = enviroment.input_width
            light = 113
            size_y = 5
            size_x = 5


        method = cv2.TM_SQDIFF_NORMED

        # find pika left
        obj_pattern = light*np.ones([size_y, size_x]).astype(np.uint8)
        image = self.resize_screen[:,start:end]

        result = cv2.matchTemplate(obj_pattern, image, method)
        position = np.where(result < 0.1)
        pos_num = len(position[0])
        if pos_num == 0:
            return [-1, -1]
        x = sum(position[1])/pos_num
        y = sum(position[0])/pos_num
        if obj == Object.Left_pika:
            x = x + 8
            y = y + 4
        elif obj == Object.Right_pika:
            x = x + int(enviroment.input_width/2) + 8
            y = y + 4

        return [int(x), int(y)]

    def crash_detect(self, np_image):
        debug_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        light = sum(sum(debug_image))
        # white image
        if light > 150000:
            print('detect white screen')
            self.white_image_time = self.white_image_time + 1
        else:
            self.white_image_time = 0

        if self.white_image_time >=3:
            print('detect crash')
            self.crash = True


class Object:
    Left_pika = 0
    Right_pika = 1
    Ball = 2
