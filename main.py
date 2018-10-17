
import os
import time
import subprocess
import cv2

import game as pika_game


class App:
    def __init__(self):
        game = pika_game.Game()
        game.start()

        time.sleep(3)
        image1 = game.get_screen()
        i = 0
        while(i < 1):
            i = i + 1
            time.sleep(0.2)
            image2 = game.get_screen()
            image_diff = image2 - image1
            filename = 'diff_' + str(i) + '.png'
            # cv2.imwrite(filename, image2)
            image1 = image2

App()
