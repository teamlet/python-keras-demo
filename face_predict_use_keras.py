#-*- coding: utf-8 -*-

#函数名：face_predict_use_keras.py
#作用　：从视频流中识别我-liuhc或者朋友-zyq
#用法　：python face_predict_use_keras.py
#依赖　：sys ,face_train_use_keras.py ,opencv

import cv2
import sys
import random
#import gc
from face_train_use_keras import Model
import dlib
from load_face_dataset import IMAGE_SIZE
from new_face_data import relight
if __name__ == '__main__':
#    if len(sys.argv) != 2:
#        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
#        sys.exit(0)
#        
    #加载模型
    model = Model()
    model.load_model(file_path = './model/f1.face.model.h5')
              
    #框住人脸的矩形边框颜色       
    color = (0, 255, 0)
    
    #捕获指定摄像头的实时视频流
#    cap = cv2.VideoCapture(int(sys.argv[1]))
    cap = cv2.VideoCapture(0)
    
    detector=dlib.get_frontal_face_detector()
    #人脸识别分类器本地存储路径
#    cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"    
    
    #循环检测识别人脸
    num=0;
    check_liuhc_num=0;
    check_zyq_num=0;
    check_other_num=0;
    while num<=10:
        
#    while True:
        _, frame = cap.read()   #读取一帧视频
        
        #图像灰化，降低计算复杂度
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#        #使用人脸识别分类器，读入分类器
#        cascade = cv2.CascadeClassifier(cascade_path)                
#
#        #利用分类器识别出哪个区域为人脸
#        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))        
#        if len(faceRects) > 0:                 
#            for faceRect in faceRects: 
#                x, y, w, h = faceRect
#                
#                #截取脸部图像提交给模型识别这是谁
#                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
#                dets=detector(grey,1)
#        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)           
        dets=detector(frame_gray,1)
        for i,d in enumerate(dets):
            x1=d.top() if d.top()>0 else 0
            y1=d.bottom() if d.bottom()>0 else 0
            x2=d.left() if d.left()>0 else 0
            y2=d.right() if d.right()>0 else 0
            image=frame[x1:y1,x2:y2];
            image=cv2.resize(image,(IMAGE_SIZE,IMAGE_SIZE))
            # image=relight(image,random.uniform(0.8,1.2),random.randint(-50,50))
            faceID = model.face_predict(image)   
            #如果是“我”
            if faceID == 0: 
                                                        
#                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                cv2.rectangle(frame, (x2,x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'liuhc' ,(x2+20,x1+250), font, 1, (255,0,255),4)   
                check_liuhc_num+=1;
#                    #文字提示是谁
#                    cv2.putText(frame,'liuhc', 
#                                (x + 30, y + 30),                      #坐标
#                                cv2.FONT_HERSHEY_SIMPLEX,              #字体
#                                1,                                     #字号
#                                (255,0,255),                           #颜色
#                                2)                                     #字的线宽
            elif faceID == 1 : 
                cv2.rectangle(frame, (x2,x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'zyq' ,(x2+20,x1+250), font, 1, (255,0,255),4) 
                check_zyq_num+=1;
            else :
                cv2.rectangle(frame, (x2,x1), (y2, y1), color)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'other' ,(x2+20,x1+250), font, 1, (255,0,255),4) 
                check_other_num+=1;
#                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
#                    
#                    #文字提示是谁
#                    cv2.putText(frame,'zyq', 
#                                (x + 30, y + 30),                      #坐标
#                                cv2.FONT_HERSHEY_SIMPLEX,              #字体
#                                1,                                     #字号
#                                (255,0,255),                           #颜色
#                                2)                                     #字的线宽
                            
            cv2.imshow("check face ", frame)
            num+=1;
        #等待10毫秒看是否有按键输入
            k = cv2.waitKey(10)
        #如果输入q则退出循环
            if k & 0xFF == ord('q')  :
                 cap.release()
                 cv2.destroyAllWindows()
                 break
            
    if check_liuhc_num >=5 | check_zyq_num >=5:
        print('check in')
    else :
        print('get_out')
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()
    
