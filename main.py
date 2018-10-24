import time
import cv2
import tensorflow as tf

import enviroment
import game as pika_game

class App:
    def __init__(self):
        # state_size = enviroment.input_width*enviroment.input_height
        # agent = DQNAgent(state_size, enviroment.action_size)

        # init game enviroment
        game = pika_game.Game()
        game.start()

        print('Pika experiment start')

        for i in range(2):

            game.play()


            time.sleep(1.5)
            print('step start')


            i = 0
            while True:
                i = i + 1
                time.sleep(1/enviroment.fps)
                game.state.update()

                if game.state.is_score_change:
                    print(str(game.state.left_score), ' vs ', str(game.state.right_score))
                elif game.state.is_episode_start:
                    game.reset()
                    break
                elif game.state.check_step_start():
                    print('step start')


App()
