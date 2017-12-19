import os,re
import numpy as np
from  urllib.request import urlretrieve
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from PIL import Image, ImageFont, ImageDraw



#找到要改的Unicode编码，并转换 , text是编码的字，ttf_url是字体文件
def data_convert(text,ttf_url):

    font_ttf_path = os.path.join(os.getcwd(), 'font_ttf')
    if not os.path.exists(font_ttf_path):
        os.mkdir(font_ttf_path)
    #fft文件绝对路径
    fft_name = ttf_url[-20:]
    print(fft_name)
    #下载ttf字体
    urlretrieve(ttf_url,'font_ttf/'+fft_name)

    word_num = len(text)                    #白背景
    im = Image.new("RGB", (22*word_num, 30), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype('font_ttf/'+fft_name, 22)
                                         #黑字
    dr.text((0,0), text, font=font,fill=(0,0,0))
    #保存图片并关闭
    im.save("ttf.png")
    im.close()
    word_img = plt.imread('ttf.png').mean(axis=2)
    # print(word_img.shape)
    word_split_list = np.split(word_img,word_num,axis = 1)
    #加载训练的模型
    pca = joblib.load('learn_model/font_recognizer.pca')
    svm = joblib.load('learn_model/font_recognizer.m')
    x_data = np.array(word_split_list).reshape(word_num,-1)
    # print(x_data.shape)
    X_train = pca.transform(x_data)
    #删除ttf字体文件
    # os.remove('font_ttf/'+fft_name)
    return (svm.predict(X_train))
# print(data_convert('\uEC26\uED71',"https://k3.autoimg.cn/g15/M11/F5/09/wKgH5VoXueyAMxJUAADO4NP7YRw04..ttf"))