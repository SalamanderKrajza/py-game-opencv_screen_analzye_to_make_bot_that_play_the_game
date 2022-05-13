import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui
from PIL import Image  


left = True
dimensions_left = {'left': 810, 'top': 550, 'width': 240, 'height': 300}
dimensions_right = {'left': 1150, 'top': 550, 'width': 240, 'height': 300}
dimensions_left = {'left': 800, 'top': 400, 'width': 350, 'height': 500}
dimensions_right = {'left': 1100, 'top': 400, 'width': 350, 'height': 500}
dimensions_left = {'left': 800, 'top': 660, 'width': 600, 'height': 200}
dimensions_right = {'left': 800, 'top': 660, 'width': 600, 'height': 200}
sct = mss.mss()

if left:
    scr = numpy.array(sct.grab(dimensions_left))
        
else:
    scr = numpy.array(sct.grab(dimensions_right))
    
scr_remove = scr[:,:,:3]
cv2.imshow('Screen Shot', scr)
cv2.imwrite('data\output.jpg', scr) 
sleep(10)   
cv2.waitKey(1)