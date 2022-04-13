import requests
import os
import time
import threading
from bs4 import BeautifulSoup


def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text


def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('li', class_='wp-item')
    for i in pic_list:
        a_tag = i.find('h3', class_='tit').find('a')
        link = a_tag.get('href')
        text = a_tag.get_text()
        get_pic(link, text)


def get_pic(link, text):
    '''
    获取当前页面的图片,并保存
    '''
    html = download_page(link)  # 下载界面
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find('div', id="picture").find_all('img')  # 找到界面所有图片
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir(f'pic/{text}')
    for i in pic_list:
        pic_link = i.get('src')  # 拿到图片的具体 url
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open(f"pic/{text}/{pic_link.split('/')[-1]}", 'wb') as f:
            f.write(r.content)
            time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():
    create_dir('pic')
    queue = list(range(1, 72))
    threads = []
    while queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and queue:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            url = f'http://meizitu.com/a/more_{cur_page}.html'
            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print(f'{threading.current_thread().name}正在下载{cur_page}页')
            threads.append(thread)


if __name__ == '__main__':
    main()
