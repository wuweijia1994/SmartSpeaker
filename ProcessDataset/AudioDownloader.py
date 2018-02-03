import os
import requests
from bs4 import BeautifulSoup

link = 'http://soundbible.com/tags-shower.html'
filepath = './audio/'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def build_directory(file_path):
    if not(os.path.exists(file_path)):
        os.mkdir(file_path)
        print("Build up directory successfully: " + file_path)
    else:
        print("This directory has been built: " + file_path)

def get_url(url):
# 获取网页信息，url:网页链接
    try:
        html = requests.get(url, headers=headers, timeout=30) # 用requests库向网页发送get请求
        html.raise_for_status() # 访问失败时raise状态码
        html.encoding = html.apparent_encoding # 用requests库判断的编码格式解码
        return html
    except:
        print('fail')

def find_mp3(text):
    soup = BeautifulSoup(text, "html.parser") # 实例化网页代码为bs对象
    div = soup.find_all('tr', attrs={'class' : 'row-b'}) # 找到所有class=sm2-360ui的div标签内容
    i = 0
    # audio_title = soup.find_all('tr', attrs={'class' : 'row-b'})
    for row in div:
        elem = row.find('div', attrs = {'class' : 'ui360'})
        name = row.find('strong')
        link = elem.find('a')['href'] # 找到每个音频链接
        link = get_url(link)
        with open(filepath + name.string + '.mp3', 'wb') as f:
            f.write(link.content)
        i += 1

build_directory(filepath)
text = get_url(link).text
find_mp3(text)