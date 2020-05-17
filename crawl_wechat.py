# -*- coding: utf-8 -*-
import requests
import time
import csv
import pandas as pd

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
    "Cookie": "RK=sJzMyfnNMb; ptcz=f269a94a57a273ef09be374bd24f3a37134133727219efdffe36f1e2a323b690; pgv_pvid=7955497316; pgv_pvi=8657359872; _ga=GA1.2.1278117112.1579741583; Qs_lvt_323937=1582737201; Qs_pv_323937=2803093533797569000; ua_id=H53GlgRyO84IVUu6AAAAAOZwnkyVBxGyh3riiuz-4Qw=; mm_lang=zh_CN; ts_uid=4417243657; wxuin=84425937278320; tvfe_boss_uuid=0b4bbce83e2b7a70; openid2ticket_oWtp85XzYdywciZni3kDvubVMFwM=vLdjgT0SfoB5UfvDq71RLkctSU/83JQTaMOxrLzGzYU=; o_cookie=3383109878; openid2ticket_oBSct5BkYLLzyj35nVPOS02QFmtA=qiCT/0qDyBz8TFF2isJB/NE+NcCCD+7y7jegv8ubcvM=; openid2ticket_oxjAL41r_jpbt_NvQEt5Qxda2wGY=8Fzhdbjc+/UI+O2/6f89BGSTF0fSIoMcOkCmqil1tJY=; noticeLoginFlag=1; remember_acct=773126182%40qq.com; openid2ticket_oSWx6tys3E-umfdZBgXWlGGcCuvc=/SFQOyvmZVGqfAXI5uAxDRKloDaFvI6tgbwSCxsRgRs=; openid2ticket_oIFbO4sBgjR-yxu2WkZ-Cvm2WIYI=TayDuxiElONykjxh9ruqKRadsi+P7E9ON/RqHBh2lXk=; ptui_loginuin=2825726692@qq.com; openid2ticket_okS_EwZjfkNbU3uI--5H-D1mIroA=oyc2rcgPrg5o42u/g94YUC2uVZdsi4NYR9e0/esS/O4=; openid2ticket_o5aKq5Ss6Fz1hMFPb-R9Zi3WnRPc=uZPRvvo6wWN0FBaTR7KThfetuBudpfGh46UzoF22fgM=; pgv_si=s5425905664; uuid=50f4a07e531726f8787ecb6b46e971f0; rand_info=CAESIKPGTNhh6stZp4RxnF3Lmpzl/A15ZSLCazXEzia/k2ab; slave_bizuin=3597221499; data_bizuin=3250859921; bizuin=3597221499; data_ticket=ruba6wVyZ4lLPKzGRbjg1Y9xsfnFSjxty9cy/cJaUmGmP8ri50Xcuw0XfRzeKhRK; slave_sid=Znk0X2VGcnRKbjlkTHNNeXNUYTNXbWdGS3hBcmNBV1BhYWZySDhCS1NpaGZ0c3pqM0IydnVwN29Rc2pVWGtJQWdkVWxqeW9GaGk3V2NCWmNVdlhpTGhaRldUMVVZZDBHMWlnMUk1REo1Y09pRGlWWE1HWjRUemdXUThsNEZVWDBJMGFaWHhsWHIwY0xHa0xr; slave_user=gh_7562d8c8fdd9; xid=fdd83f45803e86efcc1c795c65a981c5; rewardsn=; wxtokenkey=777",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}

data = {
    "action": "list_ex",
    "begin": 0,
    "count": 5,
    "fakeid": "",
    "type": 9,
    "query": "",
    "token": "1709960353",
    "lang": "zh_CN",
    "f": "json",
    "ajax": 1,
}

content_list = []
for i in range(1):
    data["begin"] = i*5
    time.sleep(2)
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        tempJson = {"title": item["title"], "link": item["link"], "cover": item["cover"], "digest": item["digest"], "create_time": time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item["create_time"])), "update_time": time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item["update_time"]))}
        print(tempJson)
# name=['title','link']
# test=pd.DataFrame(columns=name,data=content_list)
# test.to_csv("xingzhengzhifa.csv",mode='a',encoding='utf-8')
# print("保存成功")