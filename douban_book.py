from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
excel_name = "书籍.xlsx"
wb = Workbook()
ws1 = wb.active
ws1.title='书籍'


def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    return requests.get(url, headers=header).content


def get_con(html):
    soup = BeautifulSoup(html,'html.parser')
    book_list = soup.find('div', attrs={'class': 'article'})
    page = soup.find('div', attrs={'class': 'paginator'})
    next_page = page.find('span', attrs={'class': 'next'}).find('a')
    name = []
    for i in book_list.find_all('table'):
        book_name = i.find('div', attrs={'class': 'pl2'})
        m = list(book_name.find('a').stripped_strings)
        x = m[0]+m[1] if len(m)>1 else m[0]
        #print(x)
        name.append(x)
    return (name, next_page.get('href')) if next_page else (name, None)


def main():
    url = 'https://book.douban.com/top250'
    name_list=[]
    while url:
        html = get_html(url)
        name, url = get_con(html)
        name_list = name_list + name
    for i in name_list:
        location = f'A{name_list.index(i) + 1}'
        print(i)
        print(location)
        ws1[location]=i
    wb.save(filename=excel_name)


if __name__ == '__main__':
    main()

