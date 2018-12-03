#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 14:54:36 2018

@author: skyliuhc
"""

#-*- coding: utf-8 -*-
#
#函数名：new_face_data.py
#作用　：为模型训练准备人脸数据
#用法　：python face_data.py 
#        然后根据提示输入
#依赖　：opencv-python,dlib,random,numpy
#可能会出现采集图片全黑的情况(因为在处理随机亮度的时候会出现因为值小于0而被置零的情况)
   
import cv2
import os   
import sys
import dlib
import random
import datetime  
import numpy as np  
#from PIL import Image
from functools import reduce

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return reduce(fn, map(char2num, s))
# str2int(s)
#字符串转换成数字用于获取键盘输入的数字将其转化成int

def get_index(addpath):
   path=os.getcwd();
   path=os.path.join(path,addpath);
#   print(path) just for test
   count=0;
   for root,dirs,files in os.walk(path):
       for each in files:
           count+=1;
   nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:S')
   print('Beijing date:')
   print('\n',nowTime)
   print('\n','there are',count,'jpg faces','in\n',path)
   return count
#get_index(addpath)
#获取指定路径下的文件数
def relight(imgsrc, alpha=1, bias=0):
    imgsrc = imgsrc.astype(float)
    imgsrc = imgsrc * alpha + bias
    imgsrc[imgsrc < 0] = 0
    imgsrc[imgsrc > 255] = 255
    imgsrc = imgsrc.astype(np.uint8)
    return imgsrc
#relight(img,src,alpha,bias)
#调整图片的亮度
    
def CatchPICFromVideo(window_name="Collecting face data", camera_idx=0,num=0, catch_pic_num=200,path_name='./myfaces'):
#    path_name='./myfaces'
    camera_idx=0;       
    cap = cv2.VideoCapture(camera_idx)
    detector=dlib.get_frontal_face_detector()
    size=64;      
    #使用OpenCV人脸识别分类器
    #        classfier = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
    #        opencv自带的人脸检测器
    #        识别出人脸后要画的边框的颜色，RGB格式
    
    color = (0, 255, 0)
        
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break                
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #将当前桢图像转换成灰度图像            
        dets=detector(grey,1)
        for i,d in enumerate(dets):
            x1=d.top() if d.top()>0 else 0
            y1=d.bottom() if d.bottom()>0 else 0
            x2=d.left() if d.left()>0 else 0
            y2=d.right() if d.right()>0 else 0
    
            img_name = '%s/%d.jpg'%(path_name, num)                
    
            image=frame[x1:y1,x2:y2];
            image=relight(image,random.uniform(0.5,1.5),random.randint(-50,50))
            image=cv2.resize(image,(size,size))

            if np.mean(image) < 230 and np.mean(image) > 80:
                cv2.imwrite(img_name, image)
                num += 1

            if num > (catch_pic_num):   #如果超过指定最大保存数量退出循环
                cap.release()
                cv2.destroyAllWindows() 
                break
    
            #画出矩形框
            cv2.rectangle(frame, (x2,x1), (y2, y1), color, 2)
    
            #显示当前捕捉到了多少人脸图片了,当前采集的数量为num
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'num:%d' % (num),(x2+20,x1+250), font, 1, (255,0,255),4)                
    
             
                            
            cv2.imshow(window_name, frame)        
            c = cv2.waitKey(10)
            if c & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
    
if __name__ == '__main__':
     str=input('Bonjour! Would u like to input your name: y/n \n')
     name=''
     if str=='y' or str=='Y':
        name=input('now,what is your name:\n')
        print('hi! Welcome my friend',name)
     else:
         if str=='n' or str=='N':
             print('let it go ! I will show u the example')
         else:
             print('bye bye!')
#             never mind ,just for fun
     if name == '':
         path='myfaces';
     else:
         path='data/'+name;
     if not os.path.exists(path):
         os.makedirs(path)
     else:
         print('you seem to have been here')
         print('caze path has existed\r\n')
     index=get_index(path);
     num=input('how many pictures would u like to take?:\r\n')
     
     catch_pic_num=str2int(num);
     path=os.path.join(os.getcwd(),path);
     CatchPICFromVideo("Collecting face data",0,index,catch_pic_num,path)
     print('after operation')
     index=get_index(path);

