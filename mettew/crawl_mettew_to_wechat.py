#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shaisxx'

from bs4 import BeautifulSoup
import requests
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=r"F:\GitHub\Douyin-Bot\mettew\crawl_mettew_to_wechat_log.log")
logger = logging.getLogger(__name__)

APP_ID = 'wx64644a4951bf7c0a'
APP_SECRET = '2e450c2ea49abd4074138199ab88033f'
ENV = 'mettew-dep-ka1x7'
TEST_COLLECTION = "test_collection"

HEADER = {'content-type': 'application/json'}

WECHAT_URL="https://api.weixin.qq.com/"

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

'''
获取小程序token
'''
def get_access_token():
    url = '{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL,APP_ID,APP_SECRET)
    response = requests.get(url)
    result = response.json()
    logger.info(result)
    return result['access_token']

'''
保存公司信息
'''
def save_company(access_token, name, desc, create_time):
    try:
        url = '{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL, access_token)
        query = '''db.collection("t_company").add(
            {data:{name: "name_value",comment_total: 0,desc: "desc_value",create_time: "create_time_value",logo_url: "https://6d65-mettew-pro-nhaj6-1301883756.tcb.qcloud.la/logo.png?sign=a0d4baf3be3f4897c6ea4bdd69a5e599&t=1588131220"}})'''\
            .replace("name_value", name)\
            .replace("desc_value", desc)\
            .replace("create_time_value", create_time)

        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        logger.info('添加公司信息，SQL：【{}】，结果：【{}】'.format(query, response.text))
        result = response.json()
        if len(result['id_list']) > 0:
            return result['id_list'][0]
        else:
            return ''
    except Exception as ex:
        logger.error("添加公司信息，异常：【】".format(ex))

'''
更新公司评论数量
'''
def update_company(access_token, company_id, company_name, total):
    try:
        url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, access_token)
        query = '''db.collection('t_company').doc("company_id_value").update({data: {comment_total: comment_total_value}})''' \
            .replace("company_id_value", company_id) \
            .replace("comment_total_value", total)
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        logger.info('更新公司【{}】评论数量【{}】，结果：【{}】'.format(company_name, total, response.text))
    except Exception as ex:
        logger.error("更新公司【{}】评论数量【{}】，异常：【{}】".format(company_name, total, ex))

'''
更新公司时间
'''
def update_company_create_time(access_token, company_id, company_name, create_time):
    try:
        url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, access_token)
        query = '''db.collection('t_company').doc("company_id_value").update({data: {create_time: "create_time_value"}})''' \
            .replace("company_id_value", company_id) \
            .replace("create_time_value", create_time)
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        logger.info('更新公司【{}】时间【{}】，结果：【{}】'.format(company_name, create_time, response.text))
    except Exception as ex:
        logger.error("更新公司【{}】时间【{}】，异常：【{}】".format(company_name, create_time, ex))

'''
根据公司名称查询公司ID
'''
def query_company_by_name(access_token, name):
    try:
        url = '{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL, access_token)
        # 模糊查询
        # query = '''db.collection("t_company").where({name: db.RegExp({regexp: "search_key", options: "i",})}).get()'''.replace("search_key", name)
        query = '''db.collection("t_company").where({name: "name_value"}).get()'''.replace("name_value", name)
        # logger.info('根据公司名称查询公司ID，SQL：【{}】'.format(query))
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        result = response.json()
        if result['data'] != '' and len(result['data']) > 0:
            resultValue = json.loads(result['data'][0])
            return resultValue['_id']
        else:
            return ''
    except Exception as ex:
        logger.error("根据公司名称查询公司ID，异常：【{}】".format(ex))

def isExistsCompany(access_token, name):
    company_id = query_company_by_name(access_token, name)
    if len(company_id) <= 0:
        return False
    else:
        return True

'''
保存评论信息
'''
def save_comment(access_token, company_id, comment_content, is_like, create_time):
    try:
        url = '{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL, access_token)
        query = '''db.collection("t_comment").add(
            {data:{company_id: "company_id_value",comment_content: "comment_content_value",is_like: "is_like_value",create_time: "create_time_value"}})'''\
            .replace("company_id_value", company_id)\
            .replace("comment_content_value", comment_content)\
            .replace("is_like_value", is_like)\
            .replace("create_time_value", create_time)
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        # logger.info('添加评论信息，SQL：【{}】，结果：【{}】'.format(query, response.text))
        result = response.json()
        if len(result['id_list']) > 0:
            return result['id_list'][0]
        else:
            return ''
    except Exception as ex:
        logger.error("添加评论信息，异常：【{}】".format(ex))

'''
根据评论内容查询评论ID
'''
def query_comment_by_content(access_token, company_id, content, create_time):
    try:
        url = '{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL, access_token)
        # 模糊查询
        # query = '''db.collection("t_comment").where({comment_content: db.RegExp({regexp: "search_key", options: "i",})}).get()'''.replace("search_key", content)
        query = '''db.collection("t_comment").where(
            {company_id: "company_id_value",comment_content: "comment_content_value",create_time: "create_time_value"}).get()'''\
            .replace("company_id_value", company_id)\
            .replace("comment_content_value", content)\
            .replace("create_time_value", create_time)

        # logger.info('根据评论内容查询评论ID，SQL：【{}】'.format(query))
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        result = response.json()
        if result['data'] != '' and len(result['data']) > 0:
            resultValue = json.loads(result['data'][0])
            return resultValue['_id']
        else:
            return ''
    except Exception as ex:
        logger.error("根据评论内容查询评论ID，异常：【{}】".format(ex))

'''
根据公司ID获取最近评论时间
'''
def query_comment_date_by_company_id(access_token, company_id):
    try:
        url = '{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL, access_token)
        # 模糊查询
        # query = '''db.collection("t_comment").where({comment_content: db.RegExp({regexp: "search_key", options: "i",})}).get()'''.replace("search_key", content)
        query = '''db.collection('t_comment')
                      .where({company_id: "company_id_value"})
                      .field({create_time: true})
                      .orderBy('create_time', 'desc').limit(1).get()''' \
            .replace("company_id_value", company_id)

        # logger.info('根据公司ID获取最近评论时间，SQL：【{}】'.format(query))
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        result = response.json()
        if result['data'] != '' and len(result['data']) > 0:
            resultValue = json.loads(result['data'][0])
            return resultValue['create_time']
        else:
            return ''
    except Exception as ex:
        logger.error("根据公司ID获取最近评论时间，异常：【{}】".format(ex))

def isExistsComment(access_token, company_id, content, create_time):
    comment_id = query_comment_by_content(access_token, company_id, content, create_time)
    if len(comment_id) <= 0:
        return False
    else:
        return True

'''
保存回复信息
'''
def save_reply(access_token, comment_id, reply_content, create_time):
    try:
        url = '{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL, access_token)
        query = '''db.collection("t_reply").add(
            {data:{comment_id: "comment_id_value",reply_content: "reply_content_value",create_time: "create_time_value"}})''' \
            .replace("comment_id_value", comment_id) \
            .replace("reply_content_value", reply_content) \
            .replace("create_time_value", create_time)
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        logger.info('添加回复信息，SQL：【{}】，结果：【{}】'.format(query, response.text))
        result = response.json()
        if len(result['id_list']) > 0:
            return result['id_list'][0]
        else:
            return ''
    except Exception as ex:
        logger.error("添加回复信息，异常：【{}】".format(ex))

'''
根据回复内容查询回复ID
'''
def query_reply_by_content(access_token, comment_id, content, create_time):
    try:
        url = '{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL, access_token)
        # 模糊查询
        # query = '''db.collection("t_reply").where({reply_content: db.RegExp({regexp: "search_key", options: "i",})}).get()'''.replace("search_key", content)
        query = '''db.collection("t_reply").where(
            {comment_id: "comment_id_value",reply_content: "reply_content_value",create_time: "create_time_value"}).get()'''\
            .replace("comment_id_value", comment_id)\
            .replace("reply_content_value", content)\
            .replace("create_time_value", create_time)
        # logger.info('根据回复内容查询回复ID，SQL：【{}】'.format(query))
        data = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        result = response.json()
        if result['data'] != '' and len(result['data']) > 0:
            resultValue = json.loads(result['data'][0])
            return resultValue['_id']
        else:
            return ''
    except Exception as ex:
        logger.error("根据回复内容查询回复ID，异常：【{}】".format(ex))

def isExistsReply(access_token, comment_id, content, create_time):
    reply_id = query_reply_by_content(access_token, comment_id, content, create_time)
    if len(reply_id) <= 0:
        return False
    else:
        return True

def crawl_mettew(access_token):
    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=False, cookies=cookies)
    # 内容
    divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
    for div in divs:
        for ul in div.find_all('ul'):
            temp_url = base_url + ul.li.a['href']
            # logger.info('公司名称：【{}】，URL：【{}】'.format(ul.li.a.string, temp_url))
            company_url_id = temp_url[temp_url.rindex('/') + 1: len(temp_url)]
            if int(company_url_id) <= 2161:
                all_url.append(temp_url)

    for c_url in all_url:
        try:
            start_time = time.time()
            company_div_class = 'nav_area_content'
            response = session.get(c_url, headers=headers, allow_redirects=False, cookies=cookies)
            beaut = BeautifulSoup(response.text, 'lxml')
            divs = beaut.find_all('div', class_=company_div_class)

            company_name = ''
            for div in divs:
                company_name = div.strong.string

            comments_div_class = 'comments_left pull-left'
            beaut = BeautifulSoup(response.text, 'lxml')
            divs = beaut.find_all('div', class_=comments_div_class)

            main_comment = ''
            for div in divs:
                main_comment = div.h4.string.replace("\r\n", "&nbsp;&nbsp;")

            company_id = ''
            if isExistsCompany(access_token, company_name):
                company_id = query_company_by_name(access_token, company_name)
                logger.info("公司【{}】已存在，公司ID：【{}】".format(company_name, company_id))
            else:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if len(company_name) > 0:
                    company_id = save_company(access_token, company_name, main_comment, create_time)

            divs = beaut.find_all('div', class_='commentType')
            for div in divs:
                item_divs = div.find_all('div')
                comment_id = ''
                up_or_down = ''
                for item_div in item_divs:
                    if item_div.attrs:
                        item_div_class = ' '.join(item_div['class'])

                        if 'comment_icon pull-left' == item_div_class:
                            if 'fa-thumbs-up' in item_div.i['class']:
                                up_or_down = 'up'
                            if 'fa-thumbs-down' in item_div.i['class']:
                                up_or_down = 'down'

                        if 'comment_txt pull-left' == item_div_class:
                            comment_content = item_div.p.string.replace("\r\n", "&nbsp;&nbsp;")
                            comment_date = item_div.div.div.text
                            if isExistsComment(access_token, company_id, comment_content, comment_date):
                                comment_id = query_comment_by_content(access_token, company_id, comment_content, comment_date)
                                logger.info("公司【{}】的评论【{}】已存在，评论ID：【{}】".format(company_name, comment_content, comment_id))
                            else:
                                if len(company_id) > 0 and len(item_div.p.string) > 0:
                                    comment_id = save_comment(access_token, company_id, comment_content, up_or_down, comment_date)

                        if 'comment_child' == item_div_class:
                            comment_reply_content = item_div.p.string.replace("\r\n", "&nbsp;&nbsp;")
                            comment_reply_date = item_div.div.div.text
                            if isExistsReply(access_token, comment_id, comment_reply_content, comment_reply_date):
                                reply_id = query_reply_by_content(access_token, comment_id, comment_reply_content, comment_reply_date)
                                try:
                                    logger.info("公司【{}】的评论【{}】的回复【{}】已存在，回复ID：【{}】".format(company_name, comment_content, comment_reply_content, reply_id))
                                except:
                                    pass
                            else:
                                if len(comment_id) > 0 and len(item_div.p.string):
                                    save_reply(access_token, comment_id, comment_reply_content, comment_reply_date)
            if len(divs) > 0:
                update_company(access_token, company_id, company_name, str(len(divs)))
            company_create_time = query_comment_date_by_company_id(access_token, company_id);
            if len(company_create_time) > 0:
                update_company_create_time(access_token, company_id, company_name, company_create_time)
            logger.info("处理公司【{}】评论及回复数据，共耗时：【{}秒】，之后休眠1秒".format(company_name, int(time.time()-start_time)))
            time.sleep(1)
        except Exception as ex:
            logger.error("处理公司【{}】，异常：【{}】".format(c_url, ex))

if __name__ =='__main__':
    start_time = time.time()
    access_token = get_access_token()
    crawl_mettew(access_token)
    logger.info("爬取mettew数据至微信小程序云数据库，共耗时：【{}秒】".format(int(time.time()-start_time)))

    # logger.info(query_company_by_name(access_token, '北京八亿时空液晶公司111'))
    # logger.info(query_company_by_name(access_token, '重庆峘渝携(花谷鑫)'))

    # save_company(access_token, '北京八亿时空液晶公司111', '北京八亿时空液晶公司111sadfasdf', '2020-12-11 16:10:32')

    # update_company(access_token, 'c89bd61c5fd382ca012d3238471187a7', '重庆峘渝携(花谷鑫)', '121')

    # print(query_comment_date_by_company_id(access_token, 'b1a52c595fd39e5801a87b243679c904'))
    # print(query_comment_date_by_company_id(access_token, 'b1a52c595fd39c4e01a86909786a04fa'))
