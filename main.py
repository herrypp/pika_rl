import time
import cv2
import tensorflow as tf

import enviroment
import game as pika_game
from ActorNetwork import ActorNetwork
from CriticNetwork import CriticNetwork
from ReplayBuffer import ReplayBuffer

class App:
    def __init__(self):
        train_indicator = 1   #1 means Train, 0 means simply Run
        epsilon = 1

        # initial model
        sess = tf.Session()
        from keras import backend as K
        K.set_session(sess)

        actor = ActorNetwork(sess, (enviroment.input_width*enviroment.input_height), 
            enviroment.action_size, enviroment.batch_size, enviroment.TAU, enviroment.LRA)
        critic = CriticNetwork(sess, (enviroment.input_width*enviroment.input_height),
            enviroment.action_size, enviroment.batch_size, enviroment.TAU, enviroment.LRC)
        buff = ReplayBuffer(enviroment.buffer_size)    #Create replay buffer

        # load existing model
        try:
            actor.model.load_weights("actormodel.h5")
            critic.model.load_weights("criticmodel.h5")
            actor.target_model.load_weights("actormodel.h5")
            critic.target_model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

        # init game enviroment
        game = pika_game.Game()
        game.start()

        print('Pika experiment start')

        for i in range(enviroment.episode_count):
            print("Episode : " + str(i) + " Replay Buffer " + str(buff.count()))

            game.play()

            s_t = np.hstack(np.flatten(game.state.resize_screen))
            total_reward = 0.

            time.sleep(1)
            print('step start')


            while True:
                time.sleep(1/enviroment.fps)
                game.state.update()

                # loss = 0 
                # epsilon -= 1.0 / enviroment.explore
                # a_t = np.zeros([1,enviroment.action_size])
                # noise_t = np.zeros([1,enviroment.action_size])

                # a_t_original = actor.model.predict(s_t.reshape(1, s_t.shape[0]))
                # noise_t = train_indicator * max(epsilon, 0) * self.ou(a_t_original,  0.0 , 0.60, 0.30)

                # a_t = a_t_original + noise_t

                # action = np.argmax(a_t)
                # game.act(action)

                # ob, r_t, done, info = env.step(a_t[0])

                # s_t1 = np.hstack((ob.angle, ob.track, ob.trackPos, ob.speedX, ob.speedY, ob.speedZ, ob.wheelSpinVel/100.0, ob.rpm))
        
                # buff.add(s_t, a_t[0], r_t, s_t1, done)      #Add replay buffer

                # game.random_press()

                if game.state.is_score_change:
                    print(str(game.state.left_score), ' vs ', str(game.state.right_score))
                elif game.state.is_episode_start:
                    game.reset()
                    break
                elif game.state.check_step_start():
                    print('step start')

    def ou(self, x, mu, theta, sigma):
        return theta * (mu - x) + sigma * np.random.randn(1)


App()
