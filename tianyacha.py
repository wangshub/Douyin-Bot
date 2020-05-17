# -*- coding: utf-8 -*-
import re
import csv
import scrapy


class SearchSpider(scrapy.Spider):
    name = 'search'
    # num = 0
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['http://www.tianyancha.com/']
    dr = re.compile(r'<[^>]+>', re.S)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Host':'www.tianyancha.com',
        'Referer':'www.tianyancha.com',
    }
    cookies='ssuid=1206281425; TYCID=e971c240220c11ea93782b205bbc7c82; undefined=e971c240220c11ea93782b205bbc7c82; _ga=GA1.2.552681630.1576724945; aliyungf_tc=AQAAAI0XKGtgnQcAsiPMcWh8vThOoQNX; csrfToken=cAc9vd8jXwdre0AwEsaJJsbl; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1587606598; _gid=GA1.2.1067131790.1587606598; bannerFlag=true; tyc-user-phone=%255B%252215210434997%2522%255D; token=81ba4c73438b40ec98c138e720d6909b; _utm=6add275f3a414b159354c472ecd2a5c3; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%2522158%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxMDQzNDk5NyIsImlhdCI6MTU4NzYwNzM4NywiZXhwIjoxNjE5MTQzMzg3fQ.G8hp9bw7IxNVj3TxHMQTsLNzIfwTk5tUmyM0JL7f-1TKDLf7VWXKrGZjJpzx3w2fRZ8Qs-9Tv6CVnxhNseRALQ%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E9%2583%2591%25E8%2590%25BC%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215210434997%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxMDQzNDk5NyIsImlhdCI6MTU4NzYwNzM4NywiZXhwIjoxNjE5MTQzMzg3fQ.G8hp9bw7IxNVj3TxHMQTsLNzIfwTk5tUmyM0JL7f-1TKDLf7VWXKrGZjJpzx3w2fRZ8Qs-9Tv6CVnxhNseRALQ; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1587611840; _gat_gtag_UA_123487620_1=1'

    cookie={}
    # f = open('C:tianyancha_car.txt', 'w', encoding='utf-8')
    for c in cookies.split(';'):
        cookie[c.split('=')[0]]=c.split('=')[1]
    # def start_requests(self):
        # for id in idlist:

        # with open('/Users/admin/Downloads/tianyancha/tianyancha/needs.csv')as g:
        #     reader = csv.reader(g)
        #     num = 0
        #     for row in reader:
        #         num+=1
        #         id = row[3]
        #         # 爬过的去重
        #         reuslt = redis_cli.sismember('tianyancha', id)
        #         # print(reuslt)
        #         if not reuslt:
        #             print(row)
        #             meta={'oldinfo':row,'num':num}
        #             yield scrapy.Request(url='https://www.tianyancha.com/search?key=%s'%id,
        #                                  callback=self.index_parse,headers=self.headers,cookies=self.cookie,
        #                                  meta=meta)
    def index_parse(self, response):
        try:
            url = response.xpath('//a[@class="name "]/@href').extract()[0]
            # for element in response.css('#web-content > div > div.container-left > div > div.result-list>div'):
            #     url=element.css('div.header>a.name::attr(href)').extract()[0]
            yield scrapy.Request(url=url,
                                 callback=self.parse_campany,headers=self.headers,cookies=self.cookie,
                                 meta=response.meta)
        except:
            oldinfo = response.meta['oldinfo']
            print('提取详情页失败{}'.format(oldinfo))
            redis_cli.sadd('tianyancha',oldinfo[3])

            with open('searchfailed.csv','a',encoding='utf-8',newline='')as j:
                writer = csv.writer(j)
                writer.writerow(oldinfo)
                print('存入失败csv')


    def parse_campany(self, response):
        # print(response.text)
        oldinfo = response.meta['oldinfo']

        # try:
        # 企业名称
        # campany=response.css('#company_web_top > div.box > div.content > div.header > h1.name::text').extract()[0]
        # zzjgdm=response.meta['id']
        # 行业
        try:
            hy=response.css('#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(3) > td:nth-child(4)::text').extract()[0]
        except:
            hy=''
        # 登记机关
        try:
            djjj=response.css('#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(6) > td:nth-child(4)::text').extract()[0]
        except:
            djjj=''
        # 地址
        try:
            zcdz=response.css('#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(8) > td:nth-child(2)::text').extract()[0]
        except:
            zcdz=''
        # 经营范围
        try:
            jyfw = response.xpath('//span[@class="js-full-container"]/text()').extract()[0]
            if not jyfw:
                jyfw=self.dr.sub('',response.css('#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2)').extract()[0])
            # if '详情' in jyfw:
        except:
            jyfw=''
        # 简介
        try:
            introduction=response.xpath('//div[@class="summary"]/span[2]/text()').extract()[0]
            if introduction != '暂无信息':
                introduction=response.xpath('//div[@class="summary"]/script[1]/text()').extract()[0].strip()

        except:
            introduction=''
        #状态
        try:
            status = response.xpath('//div[contains(./text(),"公司状态")]/following::div[1]/@title').extract()[0]
        except:
            status=''
        # 电话
        # phone = response.xpath('//div[@class="detail"]/div[1]/div[1]/span[2]/text()').extract()[0]
        try:
            phone = response.xpath('//span[contains(./text(),"电话：")]/following::span[1]/text()').extract()[0]
        except:
            phone=''
        # 网址
        # site = response.xpath('//div[@class="detail"]/div[2]/div[1]/span[2]/text()').extract()[0]
        try:
            site = response.xpath('//span[contains(./text(),"网址")]/following::span[1]/text()').extract()[0]
        except:
            site=''
        # 注册资本
        try:
            register_money = response.xpath('//tbody/tr[1]/td[2]/div[2]/@title').extract()[0]
        except:
            register_money=''
        # 注册时间
        # register_time = response.xpath('')
        try:
            register_time = '加密'
        except:
            register_time = ''
        # 公司类型
        try:
            company_type = response.xpath('//td[contains(./text(),"公司类型")]/following::td[1]/text()').extract()[0]
        except:
            company_type = ''
        #组织机构代码
        try:
            company_code = response.xpath('//td[contains(./text(),"组织机构代码")]/following::td[1]/text()').extract()[0]
        except:
            company_code = ''
        for i in [hy,djjj,zcdz,jyfw,introduction,status,phone,site,register_money,register_time,company_type,company_code]:
            oldinfo.append(i)
        with open('result2.csv','a',encoding='utf-8',newline='')as h:
            writer = csv.writer(h)
            writer.writerow(oldinfo)
            num = response.meta['num']
            print('第{}个写入完成  ---- {}'.format(num,oldinfo[3]))
            redis_cli.sadd('tianyancha',oldinfo[3])
        # except Exception as e :
        #     print('数据解析失败',e)
        #     with open('failed.csv','a',encoding='utf-8',newline='')as j:
        #         writer = csv.writer(j)
        #         writer.writerow(oldinfo)
        #         print('存入失败csv')


# import csv
# all=[]
# with open('/Users/admin/Downloads/tianyancha/tianyancha/needs.csv')as g:
#     reader = csv.reader(g)
#
#     for row in reader:
#         all.append(row[3])
# print(len(all))
# print(len(set(all)))
