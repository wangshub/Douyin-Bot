#爬取百度图片

import re
import requests
import os


def getHTMLText(url):
    try:
        r = requests.get(url)
        return r.text
    except Exception:
        return ""


html = getHTMLText("http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1552549128724_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=忽米网")
# print(html)
pt = '\"objURL\":\"(https?://[^\"]*)\"'
i = 0
# 创建存放图片的文件夹
path = '.\\img'
folder = os.path.exists(path)
if not folder:
    os.makedirs(path)
for x in re.findall(pt, html):
    print(x)
    try:
        r = requests.get(x, stream=True)
        pos = x.rfind(".")#获取后缀名
        with open('.\\img\\{0}{1}'.format(i, x[pos:]), "wb") as f:
            for chunk in r.iter_content():#使用iter_content,边下载边存硬盘
                f.write(chunk)
    except:
        pass
    i += 1