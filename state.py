import cv2
import mss
import numpy as np
import time
import threading
from PIL import Image 

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
        self.dark_image_time = 0
        self.i = 0

    def update(self):
        self.update_screen()
        self.update_score()
        self.update_input()

    def update_screen(self):
        # screenshot the pikaball window
        sct = mss.mss()
        mon = {"top": enviroment.screen_top,
               "left": enviroment.screen_left,
               "width": enviroment.screen_right - enviroment.screen_left,
               "height": enviroment.screen_bottom - enviroment.screen_top}
        grab_screen = sct.grab(mon)
        #pil_image = pyscreenshot.grab(bbox=(enviroment.screen_left, enviroment.screen_top,
        # enviroment.screen_right, enviroment.screen_bottom))
        img = Image.frombytes("RGB", grab_screen.size, grab_screen.bgra, "raw", "BGRX")
        #img.save('testtt_'+str(self.i)+'.png')
        np_image = np.asarray(img)
        #mss.tools.to_png(grab_screen.rgb, grab_screen.size, output=)

        #np_image = np.asarray(printscreen)
        self.crash_detect(np_image)
        # We just concern about pikachu & ball
        filter_image = self.img_filtering(np_image)
        # cv2.imshow('resize image', cv2.resize(filter_image, (enviroment.input_height, enviroment.input_width)))
        # cv2.waitKey(1)
        cv2_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)
        self.i = self.i + 1
        #cv2.imwrite('cv2_filter_image_'+ str(self.i) +'.png', cv2_image)

        self.screen = cv2_image
        self.resize_screen = cv2.resize(cv2_image, (enviroment.input_width, enviroment.input_height))
        

    def update_score(self):
        self.is_score_change = False
        self.reward = 1
        left_score_img = self.screen[11:51, 60:95]
        right_score_img = self.screen[11:51, 485:520]
        #cv2.imwrite('cv2_left_'+ str(self.i) +'.png', left_score_img)
        #cv2.imwrite('cv2_right_'+ str(self.i) +'.png', right_score_img)

        new_score = self.get_score(left_score_img)
        if new_score != -1 and self.left_score != new_score:
            self.input = None
            self.left_score = new_score
            self.is_score_change = True
            self.reward = -50
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
        img_filterd[img[:,:,2] > 127] = [0, 0, 0]
        img_filterd[img[:,:,0] < 160] = [0, 0, 0]

        return img_filterd
    
    def check_score(self, score_img, image_set):
        for img in image_set:
            if np.array_equal(score_img, img):
                return True
            
        return False

    def get_score(self, score_img):
        if self.check_score(score_img, enviroment.number_image[0]):
            return 0
        elif self.check_score(score_img, enviroment.number_image[1]):
            return 1
        elif self.check_score(score_img, enviroment.number_image[2]):
            return 2
        elif self.check_score(score_img, enviroment.number_image[3]):
            return 3
        elif self.check_score(score_img, enviroment.number_image[4]):
            return 4
        elif self.check_score(score_img, enviroment.number_image[5]):
            return 5
        else:
            return -1

    def update_input(self):
        object_list = []
        object_list.extend(self.find_object(Object.Left_pika))
        object_list.extend(self.find_object(Object.Right_pika))
        object_list.extend(self.find_object(Object.Ball))

        if self.input is None:
            object_list = object_list + object_list + object_list
            self.input = np.asarray(object_list)
        else:
            self.input[0:12] = self.input[6:18]
            self.input[12:18] = np.asarray(object_list)
                

    def find_object(self, obj):
        start = 0
        end = 0
        light = 0
        size_x = 0
        size_y = 0
        if obj == Object.Left_pika:
            start = 0
            end = int(enviroment.input_width/2)
            light = 213
            size_y = 10
            size_x = 10
        elif obj == Object.Right_pika:
            start = int(enviroment.input_width/2)
            end = enviroment.input_width
            light = 213
            size_y = 10
            size_x = 10
        else:
            start = 0
            end = enviroment.input_width
            light = 72
            size_y = 5
            size_x = 5


        method = cv2.TM_SQDIFF_NORMED

        # find pika left
        obj_pattern = light*np.ones([size_y, size_x]).astype(np.uint8)
        image = self.resize_screen[:,start:end]
        #im = Image.fromarray(image)
        #im.save('find_' + str(self.i) + '.png')

        result = cv2.matchTemplate(obj_pattern, image, method)
        #if obj == Object.Ball:
        #    print(result)
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
            
        #print('obj = ' + str(obj) + ', x = ' + str(x) + ', y = ' + str(y))
        return [int(x), int(y)]

    def crash_detect(self, np_image):
        debug_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        light = sum(sum(debug_image))
        #print('light = ' + str(light))
        # dark image
        if light < 10000:
            print('detect dark screen')
            self.dark_image_time = self.dark_image_time + 1
        else:
            self.dark_image_time = 0

        if self.dark_image_time >=3:
            print('detect crash')
            self.crash = True


class Object:
    Left_pika = 0
    Right_pika = 1
    Ball = 2
