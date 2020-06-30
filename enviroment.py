import cv2

game_cmd = "pikaball.exe"
model_name = "pika-dqn.h5"
record_name = "Reward_record.txt"
epsilon_name = "epsilon.txt"
screen_left = 700
screen_top = 414
screen_right = 1240
screen_bottom = 795

screen_width = (screen_right - screen_left)*2
screen_height = (screen_bottom - screen_top)*2
input_width = 255
input_height = 165
state_size = 18
action_size = 11
batch_size = 32

number_image = [[cv2.cvtColor(cv2.imread('image_windows/0.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/0_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/0_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/0_3.png'), cv2.COLOR_RGB2GRAY)],
                [cv2.cvtColor(cv2.imread('image_windows/1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/1_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/1_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/1_3.png'), cv2.COLOR_RGB2GRAY)],
                [cv2.cvtColor(cv2.imread('image_windows/2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/2_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/2_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/2_3.png'), cv2.COLOR_RGB2GRAY)],
                [cv2.cvtColor(cv2.imread('image_windows/3.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/3_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/3_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/3_3.png'), cv2.COLOR_RGB2GRAY)],
                [cv2.cvtColor(cv2.imread('image_windows/4.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/4_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/4_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/4_3.png'), cv2.COLOR_RGB2GRAY)],
                [cv2.cvtColor(cv2.imread('image_windows/5.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/5_1.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/5_2.png'), cv2.COLOR_RGB2GRAY),
                 cv2.cvtColor(cv2.imread('image_windows/5_3.png'), cv2.COLOR_RGB2GRAY)]]