import numpy as np
import cv2

import enviroment


class Object:
	Left_pika = 0
	Right_pika = 1
	Ball = 2

def find_object(img, obj):
	start = 0
	end = 0
	light = 0
	if obj == Object.Left_pika:
		start = 0
		end = int(enviroment.input_width/2)
		light = 232
	elif obj == Object.Right_pika:
		start = int(enviroment.input_width/2)
		end = enviroment.input_width
		light = 232
	else:
		start = 0
		end = enviroment.input_width
		light = 113

	img_r = cv2.resize(img, (enviroment.input_width, enviroment.input_height))
	img_r = cv2.cvtColor(img_r, cv2.COLOR_RGB2GRAY)

	method = cv2.TM_SQDIFF_NORMED

	# find pika left
	obj_pattern = light*np.ones([1, 4]).astype(np.uint8)
	image = img_r[:,start:end]

	result = cv2.matchTemplate(obj_pattern, image, method)
	position = np.where(result < 0.001)
	pos_num = len(position[0])
	x = sum(position[1])/pos_num
	if obj == Object.Right_pika:
		x = x + int(enviroment.input_width/2)
	y = sum(position[0])/pos_num

	print('position : ', x,'x', y)

img = cv2.imread('test.png')

find_object(img, Object.Left_pika)
find_object(img, Object.Right_pika)
find_object(img, Object.Ball)

