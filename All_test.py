#test all device
#dete 2018_11_26
#author@zhaoyiqun

import RPi.GPIO as GPIO
import time
import picamera
from array import *

import picamera
import picamera.array
from time import sleep
import numpy as np
import cv2
import io
import datetime

import sys
import random
#import gc
from face_train_use_keras import Model
import dlib
from load_face_dataset import IMAGE_SIZE
from new_face_data import relight

#to initialize the io interface
ports = [7, 22, 18, 16]
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.IN)

    #ports = [7, 22, 18, 16]
    for p in ports:
        GPIO.setup(p, GPIO.OUT)
    pass

#to open the door
def unlocking(clockwise=0,steps=90):
    arr = [0, 1, 2, 3]
    if clockwise != 1:
        arr = [3, 2, 1, 0]

    for x in range(0, steps):
        for j in arr:
            time.sleep(0.01)
            for i in range(0, 4):
                if i == j:
                    GPIO.output(ports[i], True)
                else:
                    GPIO.output(ports[i], False)

#to close the door
def locking(clockwise=1,steps=90):
    arr = [0, 1, 2, 3]
    if clockwise != 1:
        arr = [3, 2, 1, 0]

    for x in range(0, steps):
        for j in arr:
            time.sleep(0.01)
            for i in range(0, 4):
                if i == j:
                    GPIO.output(ports[i], True)
                else:
                    GPIO.output(ports[i], False)

#to detect if there is a man close to the door
def detect():
    if GPIO.input(12)==True:
        return True
    else:
        return False

#recognize the accessor and decide whether to open the door
def face_recognize():
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    sleep(5)

    # 加载模型
    model = Model()
    model.load_model(file_path='./model/new3.face.model.h5')
    # 框住人脸的矩形边框颜色
    color = (0, 255, 0)
    detector = dlib.get_frontal_face_detector()
    # 循环检测识别人脸
    num = 0;
    check_liuhc_num = 0;
    check_zyq_num = 0;
    check_other_num = 0;


    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        # ****************************#
        # add codes in this place
        # 图像灰化，降低计算复杂度
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        dets = detector(frame_gray, 1)
        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0
            image = frame[x1:y1, x2:y2];
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
            faceID = model.face_predict(image)
            # 如果是“我”
            if faceID == 0:
                cv2.rectangle(frame, (x2, x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'liuhc', (x2 + 20, x1 + 250), font, 1, (255, 0, 255), 4)
                check_liuhc_num += 1;
            elif faceID == 1:
                cv2.rectangle(frame, (x2, x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'zyq', (x2 + 20, x1 + 250), font, 1, (255, 0, 255), 4)
                check_zyq_num += 1;
            else:
                cv2.rectangle(frame, (x2, x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'other', (x2 + 20, x1 + 250), font, 1, (255, 0, 255), 4)
                check_other_num += 1;
            cv2.imshow("check face ", frame)
            num += 1;
            # 等待10毫秒看是否有按键输入
            k=cv2.waitKey(10)
            # 如果输入q则退出循环
            if num==10:
                break
        if num==10:
            break
        # ****************************#
        stream.truncate()
        stream.seek(0)

    camera.close()
    cv2.destroyAllWindows()
    print("liu:", check_liuhc_num, "zhao", check_zyq_num)
    if check_liuhc_num >=5 or check_zyq_num >=5:
        print('check in')
        return True
    else :
        print('get_out')
        return False


#test part:to test every function
def unlocking_locking_test():
    print("the function unlocking_locking_test() is working !")
    init()
    print("it is unlocking !")
    unlocking()
    time.sleep(10)
    print("it is locking !")
    locking()

def detect_unlocking_test_1():
    print("the function detect_unlocking_test_1() is working !")
    init()
    while True:
        if detect():
            print("some one is coming,open the door !")
            unlocking()
            break
    time.sleep(10)
    print("now close the door")
    locking()

def detect_unlocking_test_2():
    print("the function detect_unlocking_test_2() is working !")
    init()
    while True:
        if detect():
            print("some one is coming,open the door !")
            unlocking()
            time.sleep(10)
            print("now close the door")
            locking()

def face_recognize_test():
    print("the function face_recognize_test() is working !")
    init()
    if face_recognize():
        unlocking()
        time.sleep(5)
        locking()

def all_test():
    print("the function all_test() is working !")
    init()

    while True:
        if detect():
            access=face_recognize()
            if access:
                print("you are accepted,now open the door !")
                unlocking()
                time.sleep(10)
                print("now close the door")
                locking()

#unlocking_locking_test()
#detect_unlocking_test_1()
#detect_unlocking_test_2()
#face_recognize_test()
all_test()
