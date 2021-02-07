#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Cavin Cao'

'''
	功能：利用云开发http api操作小程序云数据库
'''

import requests
import json
import config

APP_ID = 'wx64644a4951bf7c0a'
APP_SECRET = '2e450c2ea49abd4074138199ab88033f'
ENV = 'mettew-dep-ka1x7'
TEST_COLLECTION = "test_collection"

HEADER = {'content-type': 'application/json'}

WECHAT_URL="https://api.weixin.qq.com/"

'''
获取小程序token
'''
def get_access_token():
    url='{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL,APP_ID,APP_SECRET)
    response =requests.get(url)
    result=response.json()
    print(result)
    return result['access_token']

'''
新增集合
'''
def add_collection(accessToken):
    url='{0}tcb/databasecollectionadd?access_token={1}'.format(WECHAT_URL,accessToken)
    data={
        "env":ENV,
        "collection_name":TEST_COLLECTION
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('1.新增集合：'+response.text)

'''
新增数据
'''
def add_data(accessToken):
    url='{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL,accessToken)
    query='''
    db.collection("test_collection").add({
        data:{
            key:1,
            value:"2345"
        }
    })
    '''
    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('2.新增数据：'+response.text)
    result = response.json()
    # resultValue = json.loads(result['id_list'])
    if len(result['id_list']) > 0:
        return result['id_list'][0]
    else:
        return '0'

'''
查询数据
'''
def query_data(accessToken):
    url='{0}tcb/databasequery?access_token={1}'.format(WECHAT_URL,accessToken)
    query='''
    db.collection("test_collection").limit(10).skip(1).get()
    '''

    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('3.查询数据：'+response.text)
    result=response.json()
    resultValue = json.loads(result['data'][0])
    return resultValue['_id']

'''
删除数据
'''
def delete_data(accessToken,id):
    url='{0}tcb/databasedelete?access_token={1}'.format(WECHAT_URL,accessToken)
    query='''db.collection("test_collection").doc("{0}").remove()'''.format(id)

    data={
        "env":ENV,
        "query":query
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('4.删除数据：'+response.text)

'''
删除集合
'''
def delete_collection(accessToken):
    url='{0}tcb/databasecollectiondelete?access_token={1}'.format(WECHAT_URL,accessToken)
    data={
        "env":ENV,
        "collection_name":TEST_COLLECTION
    }
    response  = requests.post(url,data=json.dumps(data),headers=HEADER)
    print('5.删除集合：'+response.text)

if __name__ =='__main__':
    #0.获取token
    accessToken=get_access_token()
    #1.新增集合：
    # add_collection(accessToken)
    #2.新增数据
    id=add_data(accessToken)
    print(id)
    # #3.查询数据
    # id=query_data(accessToken)
    # #4.删除数据
    # delete_data(accessToken,id)
    # #5.删除集合
    # delete_collection(accessToken)