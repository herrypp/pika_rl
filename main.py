import time
import cv2
import tensorflow as tf
import os.path
from matplotlib import pyplot as plt

import enviroment
import game as pika_game
from DQNAgent import DQNAgent

def read_reward():
    reward_list = []
    if os.path.exists(enviroment.record_name):
        print('load existing record file : ', enviroment.record_name)
        text_file = open(enviroment.record_name, "r")
        reward = text_file.read().split(' ')
        for r in reward:
            reward_list.append(r)

        text_file.close()
    return reward_list

def write_reward(record):
    text_file = open(enviroment.record_name, "w")
    
    for r in record:
        text_file.write(r + ' ')

    text_file.close()

def plot_reward(reward_str_list):
    past = 0
    smooth = 0.2
    reward_int_list = []
    for s in reward_str_list:
        if len(s)>0:
            smooth_reward = smooth*past + (1-smooth)*int(s)
            reward_int_list.append(smooth_reward)
    plt.plot(reward_int_list)
    plt.show()

def main():
    game_count = 6
    agent = DQNAgent(enviroment.state_size, enviroment.action_size)
    if os.path.exists(enviroment.model_name):
        print('load existing model : ', enviroment.model_name)
        agent.load(enviroment.model_name)

    # init game enviroment
    game = pika_game.Game()
    game.start()

    print('Pika experiment start')

    episode = 1
    reward_record = read_reward()

    for i in range(1, game_count+1):
        print('start new game : ', i, ' !!!')
        game.play()
        time.sleep(1.5)

        print('step start')
        training_flag = True
        episode_reward = 0
        game_reward = 0
        done = False
        game.state.update()


        while True:
            # handle wine crash
            if game.state.crash:
                print('wine crash!!!')
                break

            if training_flag:
                episode_reward = episode_reward + 1
                pre_state = game.state.input
                action = agent.act(pre_state)
                # print('action : ', action)
                game.act(action)

            time.sleep(1/enviroment.fps)
            game.state.update()

            if training_flag:
                reward = game.state.reward
                # print('reward : ', reward)
                agent.remember(pre_state, action, reward, game.state.input, done)

            if game.state.is_score_change:
                print(str(game.state.left_score), ' vs ', str(game.state.right_score))
                done = True
                episode = episode + 1
                training_flag = False
                episode_reward = episode_reward + game.state.reward
                game_reward = game_reward + episode_reward
                print("episode: {}, score: {}"
                      .format(episode, episode_reward))
            elif game.state.is_episode_start:
                reward_record.append(str(game_reward))
                episode_reward = 0
                training_flag = False
                if i % 2 == 0:
                    agent.save(enviroment.model_name)
                game.reset()
                break
            elif game.state.check_step_start():
                training_flag = True
                episode_reward = 0
                print('step start')

            if training_flag:
                if len(agent.memory) > enviroment.batch_size:
                    agent.replay(enviroment.batch_size)

        if game.state.crash:
            break
    
    if not game.state.crash:
        write_reward(reward_record)
        plot_reward(reward_record)
    
    return game.state.crash


    

crash = main()
print('crash = ', crash)
while(crash):
    crash = main()
