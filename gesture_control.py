import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from pynput.keyboard import Key, Controller

keyboard = Controller()

camera = cv2.VideoCapture(0)

# check camera resolution
(_, frame) = camera.read()
(height, width, channel) = frame.shape
print(width, height)

# Load Model
model = load_model('model/gesture_cnn.h5')
#model = load_model('model/tl_gesture.h5')	

# Dictionary
dict = {0: 'down', 1: 'left', 2: 'right', 3: 'stop', 4: 'up'}

while True:
    (_, frame) = camera.read()
    frame = cv2.flip(frame, 1) # flip the frame so that it is not the mirror view
	
    top, bottom, left, right = 20, 244, 208, 432 # 224x224
    roi = frame[top:bottom, left:right]          # region of interest
        	
#    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
	
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    frame= cv2.cvtColor(gray,  cv2.COLOR_GRAY2BGR)
#    frame[top:bottom, left:right] = roi

    x_data = roi / 255.0
    x_data = x_data.reshape(1,224,224,3)

    # prediction
    predictions = model.predict(x_data)
    maxindex = int(np.argmax(predictions))
    print(predictions[0][maxindex], dict[maxindex])
#    cv2.putText(frame, dict[maxindex], (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
#    cv2.putText(frame, str(predictions[0][maxindex]), (left, bottom+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)       
#    cv2.imshow('frame', frame)

    if (maxindex==0): # down
        keyboard.press(Key.down) #('s')
        keyboard.release(Key.down) #('s')	
    if (maxindex==1): # left
        keyboard.press(Key.left) #('a')
        keyboard.release(Key.left) #('a')		
    if (maxindex==2): # right
        keyboard.press(Key.right) #('d')
        keyboard.release(Key.right) #('d')			
    if (maxindex==3): # stop
        keyboard.press(' ')
        keyboard.release(' ')        
    if (maxindex==4): #up
        keyboard.press(Key.up) #('w')
        keyboard.release(Key.up) #('w')
	
    keypress = cv2.waitKey(1) & 0xFF # keypress by user 
    if keypress == ord("q"): # press q to quit
        break
		                     
# free up memory
camera.release()
cv2.destroyAllWindows()
