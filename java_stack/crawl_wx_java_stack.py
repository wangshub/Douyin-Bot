# -*- coding:utf-8 -*-

import requests
import time
import re
import urllib3

urllib3.disable_warnings()

req = requests.session()

base_url = 'https://wx.javastack.cn'

headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
}

def login():
    login_url = '/app/login/code2Session'

    req_data = {
        'code': '011ek2ll28ZSn64DzOml2hbE0u1ek2lf'
    }
    res_text = req.get(base_url + login_url, headers=headers, data=req_data, verify=False).text
    print(res_text)

def question_info():
    info_url = '/app/question/info'

    req_data = {
        "title": "Spring Boot 有哪些优缺点？", "category": 7
    }
    res_text = req.post(base_url + info_url, headers=headers, data=req_data, verify=False).text
    print(res_text)

if __name__ == '__main__':
    print("")
    # login()

    question_info()
