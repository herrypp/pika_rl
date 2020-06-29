import cv2

game_cmd = "wine /Users/i_herrywang/rl/pika_rl/pikaball.exe"
model_name = "pika-dqn.h5"
record_name = "Reward_record.txt"
epsilon_name = "epsilon.txt"
screen_left = 510
screen_top = 341
screen_right = 939
screen_bottom = 614
screen_width = (screen_right - screen_left)*2
screen_height = (screen_bottom - screen_top)*2
input_width = 255
input_height = 165
state_size = 18
action_size = 11
batch_size = 32

number_image = [cv2.cvtColor(cv2.imread('image/0.png'), cv2.COLOR_RGB2GRAY),
        cv2.cvtColor(cv2.imread('image/1.png'), cv2.COLOR_RGB2GRAY),
        cv2.cvtColor(cv2.imread('image/2.png'), cv2.COLOR_RGB2GRAY),
        cv2.cvtColor(cv2.imread('image/3.png'), cv2.COLOR_RGB2GRAY),
        cv2.cvtColor(cv2.imread('image/4.png'), cv2.COLOR_RGB2GRAY),
        cv2.cvtColor(cv2.imread('image/5.png'), cv2.COLOR_RGB2GRAY)]
