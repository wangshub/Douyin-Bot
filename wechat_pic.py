import sys


reload(sys)
sys.setdefaultencoding('utf-8')

from urllib import quote
from pyquery import PyQuery as pq

import requests
import time
import re
import os

from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait


# 搜索入口地址，以公众为关键字搜索该公众号
def get_search_result_by_keywords(sogou_search_url):
    # 爬虫伪装头部设置
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    # 设置操作超时时长
    timeout = 5
    # 爬虫模拟在一个request.session中完成
    s = requests.Session()
    log(u'搜索地址为：%s' % sogou_search_url)
    return s.get(sogou_search_url, headers=headers, timeout=timeout).content


# 获得公众号主页地址
def get_wx_url_by_sougou_search_html(sougou_search_html):
    doc = pq(sougou_search_html)
    return doc('div[class=txt-box]')('p[class=tit]')('a').attr('href')


# 使用webdriver 加载公众号主页内容，主要是js渲染的部分
def get_selenium_js_html(url):
    options = Options()
    options.add_argument('-headless')  # 无头参数
    driver = Chrome(executable_path='chromedriver', chrome_options=options)
    wait = WebDriverWait(driver, timeout=10)

    driver.get(url)
    time.sleep(3)
    # 执行js得到整个页面内容
    html = driver.execute_script("return document.documentElement.outerHTML")
    driver.close()
    return html


# 获取公众号文章内容
def parse_wx_articles_by_html(selenium_html):
    doc = pq(selenium_html)
    return doc('div[class="weui_media_box appmsg"]')


# 将获取到的文章转换为字典
def switch_arctiles_to_list(articles):
    # 定义存贮变量
    articles_list = []
    i = 1

    # 遍历找到的文章，解析里面的内容
    if articles:
        for article in articles.items():
            log(u'开始整合(%d/%d)' % (i, len(articles)))
            # 处理单个文章
            articles_list.append(parse_one_article(article))
            i += 1
    return articles_list


# 解析单篇文章
def parse_one_article(article):
    article_dict = {}

    # 获取标题
    title = article('h4[class="weui_media_title"]').text().strip()
    ###log(u'标题是： %s' % title)
    # 获取标题对应的地址
    url = 'http://mp.weixin.qq.com' + article('h4[class="weui_media_title"]').attr('hrefs')
    log(u'地址为： %s' % url)
    # 获取概要内容
    summary = article('.weui_media_desc').text()
    log(u'文章简述： %s' % summary)
    # 获取文章发表时间
    date = article('.weui_media_extra_info').text().strip()
    log(u'发表时间为： %s' % date)
    # 获取封面图片
    pic = parse_cover_pic(article)

    # 返回字典数据
    return {
        'title': title,
        'url': url,
        'summary': summary,
        'date': date,
        'pic': pic
    }


# 查找封面图片，获取封面图片地址
def parse_cover_pic(article):
    pic = article('.weui_media_hd').attr('style')

    p = re.compile(r'background-image:url\((.*?)\)')
    rs = p.findall(pic)
    log(u'封面图片是：%s ' % rs[0] if len(rs) > 0 else '')

    return rs[0] if len(rs) > 0 else ''


# 自定义log函数，主要是加上时间
def log(msg):
    print u'%s: %s' % (time.strftime('%Y-%m-%d_%H-%M-%S'), msg)


# 验证函数
def need_verify(selenium_html):
    ' 有时候对方会封锁ip，这里做一下判断，检测html中是否包含id=verify_change的标签，有的话，代表被重定向了，提醒过一阵子重试 '
    return pq(selenium_html)('#verify_change').text() != ''


# 创建公众号命名的文件夹
def create_dir(keywords):
    if not os.path.exists(keywords):
        os.makedirs(keywords)

        # 爬虫主函数


def run(keywords):
    ' 爬虫入口函数 '
    # Step 0 ：  创建公众号命名的文件夹
    create_dir(keywords)

    # 搜狐微信搜索链接入口
    sogou_search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=n&_sug_type_=' % quote(
        keywords)

    # Step 1：GET请求到搜狗微信引擎，以微信公众号英文名称作为查询关键字
    log(u'开始获取，微信公众号英文名为：%s' % keywords)
    log(u'开始调用sougou搜索引擎')
    sougou_search_html = get_search_result_by_keywords(sogou_search_url)

    # Step 2：从搜索结果页中解析出公众号主页链接
    log(u'获取sougou_search_html成功，开始抓取公众号对应的主页wx_url')
    wx_url = get_wx_url_by_sougou_search_html(sougou_search_html)
    log(u'获取wx_url成功，%s' % wx_url)

    # Step 3：Selenium+PhantomJs获取js异步加载渲染后的html
    log(u'开始调用selenium渲染html')
    selenium_html = get_selenium_js_html(wx_url)

    # Step 4: 检测目标网站是否进行了封锁
    if need_verify(selenium_html):
        log(u'爬虫被目标网站封锁，请稍后再试')
    else:
        # Step 5: 使用PyQuery，从Step 3获取的html中解析出公众号文章列表的数据
        log(u'调用selenium渲染html完成，开始解析公众号文章')
        articles = parse_wx_articles_by_html(selenium_html)
        log(u'抓取到微信文章%d篇' % len(articles))

        # Step 6: 把微信文章数据封装成字典的list
        log(u'开始整合微信文章数据为字典')
        articles_list = switch_arctiles_to_list(articles)
        return [content['title'] for content in articles_list]

# main入口函数：
# python
# coding: utf8
import spider_weixun_by_sogou

if __name__ == '__main__':

    gongzhonghao = raw_input(u'input weixin gongzhonghao:')
    if not gongzhonghao:
        gongzhonghao = 'spider'
    text = " ".join(spider_weixun_by_sogou.run(gongzhonghao))

    print text