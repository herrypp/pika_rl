from matplotlib import pyplot as plt
import os.path

import enviroment

reward_list = []
if os.path.exists(enviroment.record_name):
    print('load existing record file : ', enviroment.record_name)
    text_file = open(enviroment.record_name, "r")
    reward = text_file.read().split(' ')
    for r in reward:
        reward_list.append(r)

    text_file.close()

past = -450
smooth = 0.5
reward_int_list = []
for s in reward_list:
    if len(s)>0:
        smooth_reward = smooth*past + (1-smooth)*int(s)
        past = smooth_reward
        reward_int_list.append(smooth_reward)
plt.plot(reward_int_list)
plt.show()

# reward_int_list = []
# plot_list = []
# for i in range(0, len(reward_list)):
#     if len(reward_list[i])>0:
#         reward_int_list.append(int(reward_list[i]))
#         if i >= 9:
#         	plot_list.append(sum(reward_int_list[i-9:i+1])/10)
# plt.plot(reward_int_list)
# plt.show()
