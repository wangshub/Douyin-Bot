from bs4 import BeautifulSoup
import requests

import xlsxwriter

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}
div_class_name = 'col-xs-4 col-sm-4 col-md-4 col-lg-4 marg-left-40 no-pad-l-r col-md-8new'
all_url = []
url = 'https://cloud.inspur.com/market/Data/List/index/param/All-All-IIoT/p/{}.html '

for i in range(109):
    response = requests.get(url.format(i))
    # 内容
    divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
    for div in divs:
        a = div.h4.a
        next_url = 'https://cloud.inspur.com{}'.format(a['href'])
        all_url.append(next_url)
        print(next_url)

names = []
server = []
phone = []
email = []
for c_url in all_url:
    company_name_div_class = 'col-xs-10 col-sm-10 col-md-10 col-lg-10'
    response = requests.get(c_url)
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=company_name_div_class)

    if len(divs) > 0:
        print(divs[0].form.h3.string)
        names.append(divs[0].form.h3.string)
    divs = beaut.find_all('div', class_='col-xs-8 col-sm-8 col-md-8 col-lg-8 no-pad-l-r')
    for div in divs:
        if div.p.a:
            print(div.p.a.string)
            server.append(div.p.a.string)
        elif div.p.span:
            print(div.p.span.string)
            phone.append(div.p.span.string)
        else:
            try:
                if '工作日' in div.p.string:
                    pass
                else:
                    print(div.p.string)
                    email.append(div.p.string)
            except:
                print(div.p.string)
                email.append(div.p.string)

workbook = xlsxwriter.Workbook('C:/Users/windows/Desktop/com.xlsx')
worksheet = workbook.add_worksheet()
for index, content in enumerate(names):
    row = 'A' + str(index + 1)
    row1 = 'B' + str(index + 1)
    row2 = 'C' + str(index + 1)
    row3 = 'D' + str(index + 1)
    worksheet.write(row, content)
    worksheet.write(row1, server[index])
    worksheet.write(row2, phone[index])
    worksheet.write(row3, email[index])

workbook.close()
