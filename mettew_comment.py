from bs4 import BeautifulSoup
import requests
import time
import random

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}

cookies = {
    'Cookie': 'jsession=0f7317d78e03a35967b25123f5b7ff2d55caaefd7ce7d3cfff1af75d6a79e7b1'
}

base_url = 'http://www.mettew.com'
url = 'http://www.mettew.com/companies'
div_class_name = 'col-md-8 search_div'
all_url = []

s = requests.Session()

response = s.get(url, headers=headers, allow_redirects=False, cookies=cookies)
# 内容
divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
for div in divs:
    for ul in div.find_all('ul'):
        temp_url = base_url + ul.li.a['href']
        all_url.append(temp_url)

comment_list = ['欢迎访问“求职吐槽”微信小程序！',
                '抵制无良公司，欢迎访问“求职吐槽”微信小程序！',
                '微信搜索”求职吐槽“小程序，给你惊喜！',
                '抵制无良公司，微信搜索“求职吐槽”小程序！',
                '微信搜索小程序“求职吐槽”，不要让HR知道！'
            ]
for c_url in all_url:

    flag = False

    company_div_class = 'nav_area_content'
    response = s.get(c_url, headers=headers, allow_redirects=False, cookies=cookies)
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=company_div_class)

    for div in divs:
        company_name = div.strong.string
        dict_company_name={'companyName': company_name}

    comments_div_class = 'comments_left pull-left'
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=comments_div_class)

    for div in divs:
        main_comment = div.h4.string
        dict_main_comment = {'mainComment': main_comment}
    divs = beaut.find_all('div', class_='commentType')
    item_comment = []
    for div in divs:

        item_divs = div.find_all('div')
        for item_div in item_divs:
            if item_div.attrs:
                item_div_class = ' '.join(item_div['class'])

                if 'comment_txt pull-left' == item_div_class:
                    item_comment.append(item_div.p.string)

    for item in comment_list:
        if(item in item_comment):
            flag = True

    if flag == False:

        comment_url = c_url + '/comment'
        print('*********************************************************************************************************')
        print(item_comment)
        print(comment_url)

        payload = {
            'parentId': '',
            'type': 1,
            'content': random.choice(comment_list)
        }
        # 提交数据：
        respond = s.post(comment_url, data=payload, headers=headers, cookies=cookies)
        for item in comment_list:
            if(item in respond.text):
                print(item)
                print('*********************************************************************************************************\n\n')
        time.sleep(180)

