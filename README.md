这是我和赵逸群两个人完成的项目
ALL_test.py是对应在树莓派上调试的工作，这部分工作是由赵轶群完成的，最后的效果是在树莓派上可以完成红外感应，人脸识别，然后电机旋转示意开锁．
我完成的部分主要就是剩下的那些代码，因为类似的工作有很多，参考别人也一定是有的，收益最大的是Ｎeo-T的代码，讲的很详细，代码也写的不错．
他的博客是https://www.cnblogs.com/neo-T/p/6511273.html
感谢这位大神，把工作做好了并且讲明白了，能够让我们学懂．
我从获取图片的函数开始优化，增加了一下功能
：根据提示来输入姓名，还有要采集的图片
根据键入的姓名自动创建目录.提示目录下有多少张人脸．采集图片也可以接着之前的采集只不过得输入的数字大于已经存在的图片
顺便说一下ubuntu下的搜狗真是会有各种各样的bug








函数名：new_face_data.py
作用　：为模型训练准备人脸数据
用法　：python new_face_data.py(注意这里默认是python3版本，如果不是，请用python3 new_face_data.py或者直接在一些ide中直接运行)
　　　　举例：python face_data.py 
依赖　：opencv-python , sys, dlib的人脸检测器
按照提示输出姓名和数字，如果键入c的话，退出采集

函数名：load_face_dataset.py
作用　：加载图片调整指定大小并标注数据到内存
用法　：python load_face_dataset.py pathname,只不过这里只是把它封装成一个接口
依赖　：os ,sys ,numpy ,opencv

函数名：face_train_use_keras.py
作用　：
1）按照交叉验证的原则将数据集划分成三部分：训练集、验证集、测试集；
2）按照keras库运行的后端系统要求改变图像数据的维度顺序；
3）将数据标签进行one-hot编码，使其向量化
4）归一化图像数据
5）训练模型
6) 保存模型
用法　：python face_train_use_keras.py
依赖　：sklearn ,keras, random等具体见代码
   	
函数名：face_predict_use_keras.py
作用　：从视频流中识别我-liuhc或者朋友-zyq
用法　：python face_predict_use_keras.py
依赖　：sys ,face_train_use_keras.py ,opencv
