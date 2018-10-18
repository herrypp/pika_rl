import time
import cv2

import enviroment
import game as pika_game

class App:
    def __init__(self):
        game = pika_game.Game()
        game.start()

        time.sleep(1)
        print('start')

        while True:
            time.sleep(1/enviroment.fps)
            game.state.update()
            game.random_press()
            if game.state.is_game_set:
                print('game set !!')
                game.reset()
            elif game.state.is_score_set:
                print(str(game.state.left_score), ' vs ', str(game.state.right_score))
            # if take_shot:
            #     take_shot = False
            #     name = str(score) + '.png'
            #     cv2.imwrite(name, score_image)


            # avg_light = sum(sum(image))/(546*858)


App()
