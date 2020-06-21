# -*- coding: utf-8 -*-
import requests
import time
import csv
import pandas as pd

start_time = time.time()
# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
    "Cookie": "RK=sJzMyfnNMb; ptcz=f269a94a57a273ef09be374bd24f3a37134133727219efdffe36f1e2a323b690; pgv_pvid=7955497316; pgv_pvi=8657359872; _ga=GA1.2.1278117112.1579741583; Qs_lvt_323937=1582737201; Qs_pv_323937=2803093533797569000; ua_id=H53GlgRyO84IVUu6AAAAAOZwnkyVBxGyh3riiuz-4Qw=; mm_lang=zh_CN; ts_uid=4417243657; wxuin=84425937278320; tvfe_boss_uuid=0b4bbce83e2b7a70; o_cookie=3383109878; openid2ticket_oBSct5BkYLLzyj35nVPOS02QFmtA=qiCT/0qDyBz8TFF2isJB/NE+NcCCD+7y7jegv8ubcvM=; openid2ticket_oxjAL41r_jpbt_NvQEt5Qxda2wGY=8Fzhdbjc+/UI+O2/6f89BGSTF0fSIoMcOkCmqil1tJY=; noticeLoginFlag=1; remember_acct=773126182%40qq.com; openid2ticket_oSWx6tys3E-umfdZBgXWlGGcCuvc=/SFQOyvmZVGqfAXI5uAxDRKloDaFvI6tgbwSCxsRgRs=; openid2ticket_oIFbO4sBgjR-yxu2WkZ-Cvm2WIYI=TayDuxiElONykjxh9ruqKRadsi+P7E9ON/RqHBh2lXk=; ptui_loginuin=2825726692@qq.com; openid2ticket_o5aKq5Ss6Fz1hMFPb-R9Zi3WnRPc=uZPRvvo6wWN0FBaTR7KThfetuBudpfGh46UzoF22fgM=; openid2ticket_okS_EwZjfkNbU3uI--5H-D1mIroA=kEcn+AQXopqGBIrmvNlti6rOFA5wUqcVkgAZphkov5c=; pgv_si=s1602499584; pgv_info=ssid=s5066818882; uin=o0315637218; skey=@NwdaOMdr8; cert=tFBKmw2OvMXY1BscI1HltpoCx12Ky_IX; rewardsn=; mmad_session=f9b07375b181a82a8e1b096efa29a8702272dac8926442ffc3725a50e5e324fab361326fb6d242452546d0e56d84082ea64c52fb88ffe2268ba4c7eb8388de67d582caf2a0aa02dceef1a19644e0e8eb706e98808cd1f4f43e524435df4db5a311de1c56c245721266e7088080fefde3; uuid=a86e3e449a3ebcc66d7f18c7f52d057d; rand_info=CAESIP1AIvxqr5UUz2XJlzgtQxLE2Uqy8yTpP5eRZH/sfFkZ; slave_bizuin=3597221499; data_bizuin=3250859921; bizuin=3597221499; data_ticket=8g1Kjm2S01X2HZaJ10/wMZgM5N3NgUiDk3zThbQD99HDtWNohtde1PZZtfREA/JQ; slave_sid=V1ZWQzhMZE5JcGdBd1FKMkpxX1Y4WmFYdGVjcmw4TlBwM2IzalRrZENpeWVjb2FXM1pwSHo4cExxS1VMbm1GWlpaVjl2Y241Vmg0bUNQb3BKU1h2bDRFUnd4VVNYZzlUZzY4UkRZZWR5VXlSVVY3REFVNThJT3JOV3pQaVJjUHp2YkJxd0J1VU51UExPV1R4; slave_user=gh_7562d8c8fdd9; xid=a071486573cbd4c0f7db2f5f35694254",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}

data = {
    "action": "list_ex",
    "begin": 0,
    "count": 5,
    "fakeid": "",
    "type": 9,
    "query": "",
    "token": "1947533352",
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

end_time = time.time()

print("Execution Time: %.2f sec" %(end_time - start_time))

# name=['title','link']
# test=pd.DataFrame(columns=name,data=content_list)
# test.to_csv("xingzhengzhifa.csv",mode='a',encoding='utf-8')
# print("保存成功")