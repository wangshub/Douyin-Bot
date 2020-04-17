from bs4 import BeautifulSoup
import requests

import xlsxwriter
import simplejson
import time

since = time.time()

headers = {
    'Content-Type': 'application/json; charset=GBK',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

all_url = []
base_url = 'https://item.yonyoucloud.com/'
url = 'https://market.yonyoucloud.com/search/product/s?keyword=&market=&category=&productSite=&label=&page={}&price=&deliver=&os=&customerGroup=&sort=&_=1586852708126'

for i in range(832):
    response = requests.get(url.format(i)).content

    contents = simplejson.loads(response)['data']['content']

    for index, content in enumerate(contents):
        item = content['id']
        temp_url = base_url + item + ".html"
        print(str(i*10 + index) + ' : ' + temp_url)
        all_url.append(temp_url)

names = []
server = []
telephone = []
hotline = []
email = []

for index, c_url in enumerate(all_url):
    company_name_div_class = 'view-info y-right'
    response = requests.get(c_url)
    response.encoding = 'utf8'
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=company_name_div_class)

    if len(divs) > 0:
        temp_name = divs[0].h1.span.string.replace(' ', '').replace("\n", "")
        temp_server = divs[0].p.a.string
        names.append(temp_name)
        server.append(temp_server)

    divs = beaut.find_all('div', class_='contact')
    temp_telephone = ''
    temp_hotline = ''
    temp_email = ''
    for div in divs:
        for li in div.ul.find_all('li'):

            if '400电话' in li.em.string:
                temp_telephone = li.span.string

            if '服务电话' in li.em.string:
                temp_hotline = li.span.string

            if '电子邮件' in li.em.string:
                temp_email = li.span.string

    telephone.append(temp_telephone)
    hotline.append(temp_hotline)
    email.append(temp_email)
    print(str(index) + ' : ' + temp_name + ' | ' + temp_server + '|' + temp_telephone + ' | ' + temp_hotline + ' | ' + temp_email)

workbook = xlsxwriter.Workbook('E:/com11.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.set_column(0,4,40)
# worksheet.set_column("A:A", 40) #设定A列列宽为40
# worksheet.set_column("B:D", 15) #设定B、C、D三列的列宽为15
# worksheet.set_column("E:F", 50) #设定E、F列的列宽为50

for index, content in enumerate(names):
    row = 'A' + str(index + 1)
    row1 = 'B' + str(index + 1)
    row2 = 'C' + str(index + 1)
    row3 = 'D' + str(index + 1)
    row4 = 'E' + str(index + 1)
    worksheet.write(row, content, bold)
    worksheet.write(row1, server[index], bold)
    worksheet.write(row2, telephone[index])
    worksheet.write(row3, hotline[index])
    worksheet.write(row4, email[index])

workbook.close()

time.sleep(5)
time_elapsed = time.time() - since
print('爬取运行时间为：{:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))