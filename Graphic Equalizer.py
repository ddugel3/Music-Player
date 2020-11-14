import numpy as np
import cv2 as cv
import colorsys as cs
import random as rd

width = 1024
height= 600
bpp = 3

img = np.zeros((height, width, bpp), np.uint8)

thickness = -1
rect_w = 50
rect_h = 20
int_x = 55
int_y = 22
screen_start_x = 100
screen_start_y = 500

hue_start = 0
hue_stop = 0.5
saturation = 0.98
value = 0.46
count = 15


rgb_list = []
hue_size = hue_stop - hue_start
hue_diff = hue_size / count

while True:
    img = np.zeros((height, width, bpp), np.uint8)
    for i in range(count):
        hue = hue_start + hue_diff * i
        rgbcode = np.multiply(cs.hsv_to_rgb(hue, saturation, value), 256)
        eqbar_cnt = rd.randint(1, 6)

        for j in range(eqbar_cnt):
            startx = screen_start_x + i * int_x
            starty = screen_start_y - j * int_y
            cv.rectangle(img, (startx, starty), (startx + rect_w, starty + rect_h), rgbcode, thickness)

    cv.imshow("drawimg",img)
    cv.waitKey(250)

