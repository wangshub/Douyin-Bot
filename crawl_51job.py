# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

j=51
while j<60:
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    ll = []
    def geturl(url):
        res=requests.get(url,headers=headers)
        res.encoding=res.apparent_encoding
        soup=BeautifulSoup(res.text,'html.parser')
        lianjie=soup.find_all('p',class_='t1')
        for i in lianjie:
            try:
                lianjie2=i.find('a')['href']
                ll.append(lianjie2)
            except:
                pass
        return ll

    total=[]
    def getinfo(URL):
        res=requests.get(URL,headers=headers)
        res.encoding=res.apparent_encoding
        soup=BeautifulSoup(res.text,'html.parser')

        all=soup.find_all('div',class_='cn')

        for each in all:

            zhiwei=each.find('h1').text
            diqu=each.find('span',class_='lname')
            gongsi=each.find('p',class_='cname').text.strip('\n')
            #print(gongsi)
            jianjie=each.find('p',class_='msg ltype').text
            print(jianjie)
            jianjie1='--'.join(list(map(lambda x:x.strip(),jianjie.split('|'))))
            #print(jianjie1)
            xinzi=each.find('strong').text
            #print(xinzi)

        all2=soup.find_all('div',class_='tCompany_main')
        for each2 in all2:
            jingyan=each2.find_all('span',class_='sp4')
            jingyan1='--'.join(list(map(lambda x:x.text.strip(),jingyan)))
            fuli=each2.find_all('p',class_='t2')
            fuli1='--'.join('--'.join(list(map(lambda x:x.text.strip(),fuli))).split('\n'))

            zhize=each2.find_all('div',class_='bmsg job_msg inbox')

            for p in zhize:
                zhize1=p.find_all('p')
                zhize2='\n'.join(list(map(lambda x:x.text.strip(),zhize1)))
            dizhi=each2.find('div',class_='bmsg inbox')

            xinxi=each2.find('div',class_='tmsg inbox')
            #print(zhize2)

            with open('E:\\gongzuoxinxi.txt','a+',encoding='utf-8') as f:
                f.write(str(jianjie)+'\n')
                f.close()

            print("正在写入第"+str(j)+"页数据")

        info={#'zhiwei':zhiwei,
            #'diqu':diqu,
            #'gongsi':gongsi,
            #'jianjie':jianjie1,
            'xinzi':xinzi,
            #'jingyan':jingyan1,
            #'fuli':fuli1,
            'zhize':zhize2,
            #'dizhi':dizhi,
            'xinxi':xinxi}
        total.append(info)

        return total

    if __name__ == '__main__':
        url='https://search.51job.com/list/260200,000000,0000,00,9,99,%E8%AE%A1%E7%AE%97%E6%9C%BA,2,'+str(j)+'.html'#只抓一页，可以for循环抓多页

        for i in geturl(url)[1:]:
            time.sleep(2)
            getinfo(i)
    import pandas as pd
    df=pd.DataFrame(total)
    df.to_excel('E:\\zhaopinjieshao.xls')

    j=j+1