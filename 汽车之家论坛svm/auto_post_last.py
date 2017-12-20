#通过PIL中的由字体画字来生成图片，然后再用svm训练的模型识别出真正的汉字，
# 然后就可以替换了

import requests,re,os,time
import threading
from lxml import etree
from bs4 import BeautifulSoup
from svm_learn import data_convert

sem = threading.Semaphore(1)           #设置最大线程数  配置高网速好可改为其他值
BASE_DIR = os.path.join(os.getcwd(),'auto_posts')
HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'RDTaskClose_64541345=1513473318173; sessionid=6FD2961C-CD2E-4084-9DBA-C9A47184ECC5%7C%7C2017-12-15+20%3A36%3A12.744%7C%7Cwww.baidu.com; fvlid=1513341372019DcokushAMy; ahpau=1; pcpopclub=9E45335AB8513A39B21CD1122E7291DD35E8C7CC732C4E9EACA1DE9B794197ADDE5B452F9F9FE815387BF6F6181C5935AD433A96E41D052B6C426644AF24B1FE1E5F4281C9D3247001776C85871D5545BEE10B2D468170CCAF5BED106317FABDD23E82052A46CAE3C4379EFA899A4DD01BC87E845949FEB8C6FF29F3E57CAA52C24DF6EE4B85CF38539D556942BD9053C8A9D17015762D54A50BFBCD577947C32D9C6CF0C146637FEB362CFA91688DF04DA4908E1D9012D070B66685609CB8F4CF4F4346F4C44B2B0969B87F8658F2B5D9AEEB4DA4806331254747FE8F9E7ED27909F795D5185118EE7D50B7D4478EF8A01C6BEB3047F44590824AA2228EEDA64A1E5156FD3B0825154A2C019D352E7F721A5D453983C99BE76FD28DD94A37E9FBBAAF1E1874B3D37E27D546C23357BC01C01CC6; clubUserShow=64541345|4221|2|nickn2017|0|0|0||2017-12-15 20:57:07|0; autouserid=64541345; __utma=1.823915644.1513342545.1513342545.1513342545.1; __utmz=1.1513342545.1.1.utmcsr=club.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/bbs/forum-a-100002-1.html; cookieCityId=110100; sessionip=111.202.66.34; sessionuserid=64541345; sessionlogin=72ca3696868e4978a626a8396819316e03d8d2a1; sessionuid=6FD2961C-CD2E-4084-9DBA-C9A47184ECC5%7C%7C2017-12-15+20%3A36%3A12.744%7C%7Cwww.baidu.com; pvidlist=8e93f80f-7f98-4c77-a4a6-998721a3d9c812:110620:159655:0:1:846711,16bc0a62-8676-4b56-adba-f38e3046fdf712:150573:217672:0:1:888368; historybbsName4=o-200042%7C%E8%87%AA%E9%A9%BE%E6%B8%B8%2Co-200202%7C%E7%BE%8E%E9%A3%9F%2Co-200111%7C%E5%A5%B3%E6%80%A7%2Co-200201%7C%E8%BD%AE%E8%83%8E%2Co-200051%7C%E8%BD%A6%E5%B1%95%E5%BF%AB%E6%8A%A5%2Co-200213%7C%E5%AE%A0%E7%89%A9%2Co-210963%7C%E5%B7%9D%E5%B4%8E%E6%91%A9%E6%89%98%E8%BD%A6%2Co-200229%7C%E9%A9%BE%E8%80%83%2Co-200203%7C%E6%A8%A1%E5%9E%8B%2Co-200079%7C%E8%BD%A6168; autoac=B7BBE3EC3A26F222AA6C5522D06121F9; autotc=DFD1069F412CD9CAAC8A4FAA61F263FF; papopclub=8A943A896E3306C77CB3524984E752D9; pepopclub=A8C4B0761404FD448DB7A22D93268AE2; ahpvno=125; CNZZDATA1262640694=2120470880-1513338569-%7C1513478969; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1513413334,1513473293,1513475913,1513480188; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1513480355; ref=www.baidu.com%7C0%7C0%7Cwww.google.com.hk%7C2017-12-17+11%3A12%3A36.279%7C2017-12-17+09%3A14%3A50.868; sessionvid=F9736567-8546-4E97-8AFF-0841072AD823; area=110199; ahrlid=1513480355160uS8w2Cyu-1513480399704; cn_1262640694_dplus=%7B%22distinct_id%22%3A%20%221605a2cce001a9-0c3816246ec005-5b4a2c1d-1fa400-1605a2cce01264%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201513480402%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201513480402%7D%7D; UM_distinctid=1605a2cce001a9-0c3816246ec005-5b4a2c1d-1fa400-1605a2cce01264',
'Host':'club.autohome.com.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
 }

def get_ttf_url(html):
    #找ttf地址的re规则
    pat_ttf = r"format\(\'embedded-opentype\'\),url\('(//k3.autoimg.cn.*?\.ttf)'\) format\('woff'\);}"

    ttf_url_find = re.findall(pat_ttf, html, flags=re.M)
    #返回正常ttf的url地址
    return 'https:' + ttf_url_find[0]


#得到某一分类的所有论坛网址第一页
def get_forum_list(url):
    query_info = str(time.time()).replace('.','')[:13] #时间参数
    response = requests.get(url+query_info)

    pat_forum = r'//club.autohome.com.cn/bbs/forum.*?html'
    #
    forum_url_list = re.findall(pat_forum,response.text)

    for i in range(len(forum_url_list)):
        forum_url_list[i] = 'https:'+ forum_url_list[i]
    return forum_url_list

#得到某一论坛的所有页面
def parse_forum_url(forum_url):
    response = requests.get(forum_url,headers=HEADERS)
    doc = etree.HTML(response.text)
    total_page = doc.xpath('//*[@id="subcontent"]/div/span/text()')
    if len(total_page) == 1:
        total_page = total_page[0][1:-1]
    else:
        return -1
    # print(total_page)
    time.sleep(0.5)
    for page_num in range(1,int(total_page)):
        posts_page_response = requests.get(forum_url[:-5]+str(page_num)+'.html',headers=HEADERS)
        pat_post = r'/bbs/thread.*?.html'
        post_page_list = list(set(re.findall(pat_post,posts_page_response.text)))
        for i in range(len(post_page_list)):
            post_page_list[i] = 'https://club.autohome.com.cn'+post_page_list[i]
        return post_page_list

#得到一页论坛页面的所有文章地址
def get_one_page_list(url):
    response = requests.get(url,headers = HEADERS)
    pat_post = r'(/bbs/thread[^{}]*?html)'
    post_url_list = re.findall(pat_post,response.text)
    for i in range(len(post_url_list)):
        post_url_list[i] = 'https://club.autohome.com.cn' + post_url_list[i]
    return list(set(post_url_list))

#保存文章信息
def save_post(forum,title,content):
    forum_path = os.path.join(BASE_DIR, forum)
    if not os.path.exists(forum_path):
        os.mkdir(forum_path)
    post_path = os.path.join(forum_path,title+'.txt')
    with open(post_path,'w') as f:
        f.write(content)
    print('保存成功。。')


#对文章内容数据清洗
def data_cleaning(text,content,encrypt_words):
    fft_url = get_ttf_url(text)
    print(fft_url)
    #识别出文字
    true_words = data_convert(''.join(encrypt_words),fft_url)
    #替换加密的字体
    for enWord,trueWord in zip(encrypt_words,true_words):
        content = content.replace(enWord,trueWord)
    #将编码的字的显示出来
    return content.replace(u'\xa0', u' ')  #解决 gbk 不能编码u'\xa0' 的问题


#得到某一文章的forum，title和content
def get_post_content(url):
    response = requests.get(url, headers=HEADERS)
    text = response.text

    doc = BeautifulSoup(text, 'lxml')
    post_content_div = doc.select('#F0 > div.conright.fr > div.rconten > div.conttxt > div > div.tz-paragraph')[0]
    forum_name = doc.select('#consnav > span > a')[0].text
    post_title = doc.select('#consnav > span')[3].text
    # print(post_content_div)
    pat_span = r"(<span style=\"font-family: myfont;\">(.*?)</span>)"
    encrypt_span = re.findall(pat_span, str(post_content_div))
    encrypt_word = []
    post_content = post_content_div.text
    # print(post_content)
    #得到隐藏字列表enword
    for span in encrypt_span:
        encrypt_word.append(span[1])
    print(encrypt_word)
    if not post_content or not post_title:
        # print('获取' + url + '文章失败！')
        return -1
    else:
        content = data_cleaning(text, post_content, encrypt_word)
        post_title = str(post_title)
        forum_name = forum_name[0]
        print(post_title + " 获取成功！")
    #     #返回    论坛名     文章名      文章内容  加密的字Unicode码
        return forum_name, post_title, content


#集成爬取步骤，加入限制线程数量的sem
def parse_one_forum(url):
    with sem:                          #限制进程数
        post_page_list = parse_forum_url(url)    #得到一种论坛所有网页
        if post_page_list == -1:
            return -1
        for post_page in post_page_list:
            post_url_list = get_one_page_list(post_page) #得到一页论坛页面内所有帖子网址
            for post_url in post_url_list:
                try:
                    forum,title,content = get_post_content(post_url)   #得到帖子所在论坛的名字，帖子题目，内容
                    # print(content)
                except:
                    return -1
                save_post(forum,title,content)         #保存爬取的信息
                time.sleep(0.1)


def run(start_url):
    forum_url_list = get_forum_list(start_url)
    for forum_url in forum_url_list:                      #设置多线程
        th = threading.Thread(target=parse_one_forum,args=(forum_url,))
        th.start()


if __name__ == '__main__':
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    start_url = 'https://club.autohome.com.cn//ajax/ThemeBBS?callback=jsonpCallback&_='
    #只爬取一个网页验证
    url = 'https://club.autohome.com.cn/bbs/thread-c-3667-66841999-1.html'
    forum, title, content = get_post_content(url)
    print(content)
    #要保存所有文章的话用下边代码
    # run(start_url)