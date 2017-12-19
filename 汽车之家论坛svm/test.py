import os,re
import requests
from auto_post_last import get_post_content,HEADERS
from bs4 import BeautifulSoup
from svm_learn import data_convert
url = 'https://club.autohome.com.cn/bbs/thread-c-3667-66841999-1.html'
response = requests.get(url,headers = HEADERS)
doc = BeautifulSoup(response.text,'lxml')


print(data_convert(''.join(['\ueded', '\uedc1', '\uedc1', '\ueded', '\uedc1', '\ued78', '\uedc1', '\uedc1', '\uec80', '\uedc1', '\uec52', '\uedc1', '\uec52', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\uedc1', '\ueda7', '\uedc1', '\ued9d', '\uedc1', '\ueccd', '\uedc1', '\uecd9', '\uedc1', '\uece0', '\ued4b', '\uecd9', '\uec52', '\uedca', '\uedca', '\uedca']
),'https://k3.autoimg.cn/g15/M11/F5/09/wKgH5VoXueyAMxJUAADO4NP7YRw04..ttf'))