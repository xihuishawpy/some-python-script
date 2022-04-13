import requests
from openpyxl import Workbook

def get_json(url, page, lang_name):
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = [
            i['companyShortName'],
            i['companyName'],
            i['salary'],
            i['city'],
            i['education'],
        ]

        info_list.append(info)
    return info_list


def main():
    lang_name = input('职位名：')
    url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    info_result = []
    for page in range(1, 31):
        info = get_json(url, page, lang_name)
        info_result = info_result + info
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    for row in info_result:
        ws1.append(row)
    wb.save('职位信息.xlsx')

if __name__ == '__main__':
    main()
