#coding=utf-8

import json
import io
import urllib.request
import time

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]

# 根据 t_company_logo.json、t_company.json文件内容，
# 将t_company_logo文件中的公司logo 与 t_company文件同名公司的logo
# 打印 带有公司logo url地址的t_company信息

#  ******************** Begin ********************
# with open('t_company.json', encoding='utf-8') as company:
#     i = 0
#     for company_line in company:
#         i += 1
#         company_obj = json.loads(company_line)  #将json字符串转化为对象
#
#         with open('t_company_logo.json', encoding='utf-8') as logo:
#             for logo_line in logo:
#                 logo_obj = json.loads(logo_line)  #将json字符串转化为对象
#
#                 if company_obj['name'] == logo_obj['companyName']:
#                     tempUrl = logo_obj['logoUrl']
#                     try:
#                         opener.open(tempUrl)
#                         # print(str(i) + ' : ', tempUrl+'没问题')
#                         company_obj['logo_url'] = logo_obj['logoUrl']
#                     except urllib.error.HTTPError:
#                         # print(tempUrl+'=访问页面出错')
#                         time.sleep(0.1)
#                     except urllib.error.URLError:
#                         # print(tempUrl+'=访问页面出错')
#                         time.sleep(0.1)
#                     time.sleep(0.1)
#
#         with open('t_comment.json', encoding='utf-8') as comment:
#             for comment_line in comment:
#                 comment_obj = json.loads(comment_line)  #将json字符串转化为对象
#
#                 if company_obj['_id'] == comment_obj['company_id']:
#                     company_obj['create_time'] = comment_obj['create_time']
#                 else:
#                     company_obj['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#         print(company_obj)

#  ******************** End ********************


with open('t_company-26.json', encoding='utf-8') as company:
    i = 0
    for company_line in company:
        i += 1
        company_obj = json.loads(company_line)  #将json字符串转化为对象
        comment_count = 0

        comment_create_time_list = []
        with open('t_comment-26.json', encoding='utf-8') as comment:
            for comment_line in comment:
                comment_obj = json.loads(comment_line)  #将json字符串转化为对象

                if company_obj['_id'] == comment_obj['company_id']:
                    comment_count += 1
                    time.sleep(0.1)
                    # print(company_obj['_id'], comment_count, comment_obj['create_time'])
                    comment_create_time_list.append(comment_obj['create_time'])

            company_obj['comment_total'] = comment_count

        comment_create_time_list.sort()
        # print(i, company_obj['name'], comment_create_time_list[-1])
        if len(comment_create_time_list):
            company_obj['create_time'] = comment_create_time_list[-1]
        else:
            company_obj['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(company_obj)