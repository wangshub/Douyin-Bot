# -*- coding:utf-8 -*-
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import requests
import time
import urllib
import os
import json

chromeOptions = webdriver.ChromeOptions()
# 设置代理
# chromeOptions.add_argument("--proxy-server=223.243.5.161:4216")

chromedriver="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser=webdriver.Chrome(executable_path=chromedriver)
print ('请使用淘宝APP扫描登录，请勿操作鼠标键盘！请保持优雅勿频繁（间隔小于1分钟）登录以减轻服务器负载。')
wait=WebDriverWait(browser,20)

search_key = '儿童节'
data_path = 'F://crawl_data/'
data_dir = data_path + search_key + '/'

def search():
    try:
        url="https://www.taobao.com"
        browser.get(url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(search_key)
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except:
        search()

def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except:
        next_page(page_number)

def get_products():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))#加载宝贝信息并等待
    except Exception as e:
        print(e)
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()#得到所有宝贝的内容
    for item in items:
        time.sleep(3)
        product={
            'image':'https:' + item.find('.pic .img').attr('data-src'),#图片链接
            'price':item.find('.price').text(),#商品价格
            'deal':item.find('.deal-cnt').text()[:-3],#付款人数，-3是为了去掉人付款这几个字
            'title':item.find('.title').text(),#商品名称
            'shop':item.find('.shop').text(),#店铺名称
            'location':item.find('.location').text(),
            'href':'https:' + item.find('.pic .pic-link').attr('href')
        }
        print(product)
        try:
            f = open(data_dir + '/data/data.json', 'a', encoding="utf-8")
            j = json.dumps(product, ensure_ascii=False)
            f.write(str(j) + '\n')
            f.close()
        except Exception as e:
            print(e)

        try:
            f=requests.get('https:' + item.find('.pic .img').attr('data-src'))
            filename = item.find('.title').text()
            filename = eval(repr(filename).replace('\\', '-'))
            filename = eval(repr(filename).replace('/', '-'))
            filename = eval(repr(filename).replace('*', 'x'))
            filename = eval(repr(filename).replace('?', ' '))
            filename = eval(repr(filename).replace('>', ' '))
            filename = eval(repr(filename).replace('<', ' '))
            filename = eval(repr(filename).replace('|', ' '))
            filename = eval(repr(filename).replace(',', ' '))
            filename = eval(repr(filename).replace('"', ' '))
            filename = eval(repr(filename).replace(':', ' '))
            filename = eval(repr(filename).replace(';', ' '))
            filename = eval(repr(filename).replace("'", ' '))
            filename = eval(repr(filename).replace('；', ' '))
            filename = data_dir + '/img/' + filename + '.jpg'
            if not os.path.exists(filename):
                with open(filename, "wb") as code:
                    code.write(f.content)
        except Exception as e:
            print(e)

def main():
    start_time = time.time()
    # 判断目录是否存在，不存在创建目录
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(data_dir + '/img/'):
        os.mkdir(data_dir + '/img/')
    if not os.path.exists(data_dir + '/data/'):
        os.mkdir(data_dir + '/data/')

    total=search()
    print(total)
    total=int(re.compile('(\d+)').search(total).group(1)) #转换为数值型
    for i in range(2,total+1):
        next_page(i)
    end_time = time.time()
    print("Execution Time: %.2f sec" %(end_time - start_time))
if __name__=='__main__':
    main()