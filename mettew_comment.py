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
    'Cookie': 'jsession=0f7317d78e03a35967b25123f5b7ff2d55caaefd7ce7d3cfff1af75d6a79e7b1; Hm_lvt_8e5779def54689dfeb863aea23ad0397=1598852563; Hm_lpvt_8e5779def54689dfeb863aea23ad0397=1598861938; Hm_lvt_8e5779def54689dfeb863aea23ad0397=1598852563; Hm_lpvt_8e5779def54689dfeb863aea23ad0397=1599120019'
}

# 'Content-Type': 'application/json; charset=UTF-8',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

base_url = 'http://www.mettew.com'
url = 'http://www.mettew.com/companies'
div_class_name = 'col-md-8 search_div'
all_url = []

s = requests.Session()

response = s.get(url, headers=headers, allow_redirects=False, cookies=cookies)
print(response.text)
# 内容
divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
for div in divs:
    for ul in div.find_all('ul'):
        temp_url = base_url + ul.li.a['href'] + '/comment'
        # if(temp_url == 'http://www.mettew.com/companies/2325'):
        print(ul.li.a.string + ' ' + temp_url)
        all_url.append(temp_url)

comment_list = ['欢迎访问“求职吐槽”微信小程序！',
                '抵制无良公司，欢迎访问“求职吐槽”微信小程序！',
                '微信搜索”求职吐槽“小程序，给你惊喜！',
                '抵制无良公司，微信搜索“求职吐槽”小程序！',
                '微信搜索小程序“求职吐槽”，不要让HR知道！'
            ]
for c_url in all_url:
    # 构造提交数据：parentId=&type=1&content=%
    if '2981' not in c_url and '2980' not in c_url and '2979' not in c_url and '2978' \
            not in c_url and '2977' not in c_url and '2976' not in c_url:
        print(c_url)
        payload = {
            'parentId': '',
            'type': 1,
            'content': random.choice(comment_list)
        }
        # 提交数据：
        respond = s.post(c_url, data=payload, headers=headers, cookies=cookies)
        # print(respond.text)  # 输出响应
        time.sleep(180)
