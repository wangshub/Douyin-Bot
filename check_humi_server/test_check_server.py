# -*- coding: utf-8 -*-
import os,sys
import time
import sys
import pycurl
import xlwt    #导入xlwt 库

alignment = xlwt.Alignment()
# 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
alignment.horz = 0x02
# 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
alignment.vert = 0x01

style1 = xlwt.XFStyle()  # 初始化样式
font1 = xlwt.Font()  # 为样式创建字体
font1.name = '宋体'
font1.height = 20 * 14  # 字体大小，12为字号，20为衡量单位
font1.bold = True  # 黑体
font1.colour_index = 17
style1.font = font1  # 设定样式
style1.alignment = alignment

style2 = xlwt.XFStyle()  # 初始化样式
font2 = xlwt.Font()  # 为样式创建字体
font2.name = '宋体'
font2.height = 20 * 14  # 字体大小，12为字号，20为衡量单位
font2.bold = True  # 黑体
font2.colour_index = 8
style2.font = font2  # 设定样式
style2.alignment = alignment

patternFat = xlwt.Pattern()
patternFat.pattern = xlwt.Pattern.SOLID_PATTERN
patternFat.pattern_fore_colour = 1

patternUat = xlwt.Pattern()
patternUat.pattern = xlwt.Pattern.SOLID_PATTERN
patternUat.pattern_fore_colour = 41

patternPro = xlwt.Pattern()
patternPro.pattern = xlwt.Pattern.SOLID_PATTERN
patternPro.pattern_fore_colour = 44

patternError = xlwt.Pattern()
patternError.pattern = xlwt.Pattern.SOLID_PATTERN
patternError.pattern_fore_colour = 2

style3 = xlwt.XFStyle()  # 初始化样式

def checkServer(sheet, NAME, URL, n):
    if 'FAT' in NAME:
        style1.pattern = patternFat
        style2.pattern = patternFat
        style3.pattern = patternFat
    if 'UAT' in NAME:
        style1.pattern = patternUat
        style2.pattern = patternUat
        style3.pattern = patternUat
    if 'PRO' in NAME:
        style1.pattern = patternPro
        style2.pattern = patternPro
        style3.pattern = patternPro

    c = pycurl.Curl()    #创建一个Curl对象
    c.setopt(pycurl.SSL_VERIFYHOST, False)
    c.setopt(pycurl.SSL_VERIFYPEER, False)
    c.setopt(pycurl.URL, URL)    #定义请求的URL常量
    c.setopt(pycurl.CONNECTTIMEOUT, 5)    #定义请求连接的等待时间
    c.setopt(pycurl.TIMEOUT, 5)    #定义请求超时时间
    c.setopt(pycurl.NOPROGRESS, 1)    #屏蔽下载进度条
    c.setopt(pycurl.FORBID_REUSE, 1)    #完成交互后强制断开连接，不重用
    c.setopt(pycurl.MAXREDIRS, 1)    #指定HTTP重定向的最大数为1
    c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)    #设置保存DNS信息的时间为30秒
    try:
        result = c.perform_rs()    #提交请求
        print(result)
        NAMELOOKUP_TIME =  c.getinfo(c.NAMELOOKUP_TIME)    #获取DNS解析时间
        CONNECT_TIME =  c.getinfo(c.CONNECT_TIME)    #获取建立连接时间
        HTTP_CODE =  c.getinfo(c.HTTP_CODE)    #获取HTTP状态码
        SPEED_DOWNLOAD=c.getinfo(c.SPEED_DOWNLOAD)    #获取平均下载速度

        sheet.write(n, 0, str(NAME), style=style3)
        sheet.write(n, 1, "%s" %(HTTP_CODE), style=style3)
        sheet.write(n, 2, "%.2f ms"%(NAMELOOKUP_TIME*1000), style=style3)
        sheet.write(n, 3, "%.2f ms" %(CONNECT_TIME*1000), style=style3)
        sheet.write(n, 4, "%.2f M/s" %(SPEED_DOWNLOAD/1024), style=style3)
        if(HTTP_CODE == 200):
            sheet.write(n, 5, "正常", style=style1)
        else:
            sheet.write(n, 5, "异常", style=style2)

    except Exception as e:
        print("connecion error:"+str(e))
        style2.pattern = patternError
        style3.pattern = patternError
        sheet.write(n, 0, str(NAME), style=style3)
        sheet.write(n, 1, '', style=style2)
        sheet.write(n, 2, '', style=style2)
        sheet.write(n, 3, '', style=style2)
        sheet.write(n, 4, '', style=style2)
        sheet.write(n, 5, '异常', style=style2)
    finally:
        c.close()

serverList = [
                # {'name':'FAT API服务', 'url':'http://gateway.fat.humiapp.com/actuator/health'},
                {'name':' FAT humi-app-bigdata', 'url':'http://gateway.fat.humiapp.com/humi-app-bigdata/actuator/health'},
                {'name':' FAT humi-app-developer', 'url':'http://gateway.fat.humiapp.com/humi-app-developer/actuator/health'},
                {'name':' FAT humi-app-tripart', 'url':'http://gateway.fat.humiapp.com/humi-app-tripart/actuator/health'},
                {'name':' FAT humi-iem-equipment', 'url':'http://gateway.fat.humiapp.com/humi-iem-equipment/actuator/health'},
                {'name':' FAT 数据中台【humi-app-datacenter】', 'url':'http://gateway.fat.humiapp.com/humi-app-datacenter/actuator/health'},
                {'name':' FAT 基础能力【humi-app-base】', 'url':'http://gateway.fat.humiapp.com/humi-app-base/actuator/health'},
                {'name':' FAT 应用订单【humi-app-application】', 'url':'http://gateway.fat.humiapp.com/humi-app-application/actuator/health'},
                {'name':' FAT 用户中心【humi-app-user】', 'url':'http://gateway.fat.humiapp.com/humi-app-user/actuator/health'},
                {'name':' FAT 工业课堂【humi-app-community】', 'url':'http://gateway.fat.humiapp.com/humi-app-community/actuator/health'},
                {'name':' FAT 认证中心【humi-app-security】', 'url':'http://gateway.fat.humiapp.com/humi-app-security/actuator/health'},

                # {'name':'UAT API服务', 'url':'http://gateway.uat.humiapp.com/actuator/health'},
                {'name':' UAT humi-app-bigdata', 'url':'http://gateway.uat.humiapp.com/humi-app-bigdata/actuator/health'},
                {'name':' UAT humi-app-developer', 'url':'http://gateway.uat.humiapp.com/humi-app-developer/actuator/health'},
                {'name':' UAT humi-app-tripart', 'url':'http://gateway.uat.humiapp.com/humi-app-tripart/actuator/health'},
                {'name':' UAT 数据中台【humi-app-datacenter】', 'url':'http://gateway.uat.humiapp.com/humi-app-datacenter/actuator/health'},
                {'name':' UAT 基础能力【humi-app-base】', 'url':'http://gateway.uat.humiapp.com/humi-app-base/actuator/health'},
                {'name':' UAT 应用订单【humi-app-application】', 'url':'http://gateway.uat.humiapp.com/humi-app-application/actuator/health'},
                {'name':' UAT 用户中心【humi-app-user】', 'url':'http://gateway.uat.humiapp.com/humi-app-user/actuator/health'},
                {'name':' UAT 工业课堂【humi-app-community】', 'url':'http://gateway.uat.humiapp.com/humi-app-community/actuator/health'},
                {'name':' UAT 认证中心【humi-app-security】', 'url':'http://gateway.uat.humiapp.com/humi-app-security/actuator/health'},

                # {'name':'PRO API服务', 'url':'http://apis.360humi.com/actuator/health'},
                {'name':' PRO humi-app-bigdata', 'url':'https://apis.360humi.com/humi-app-bigdata/actuator/health'},
                {'name':' PRO humi-app-developer', 'url':'https://apis.360humi.com/humi-app-developer/actuator/health'},
                {'name':' PRO humi-app-tripart', 'url':'https://apis.360humi.com/humi-app-tripart/actuator/health'},
                {'name':' PRO 数据中台【humi-app-datacenter】', 'url':'https://apis.360humi.com/humi-app-datacenter/actuator/health'},
                {'name':' PRO 基础能力【humi-app-base】', 'url':'https://apis.360humi.com/humi-app-base/actuator/health'},
                {'name':' PRO 应用订单【humi-app-application】', 'url':'https://apis.360humi.com/humi-app-application/actuator/health'},
                {'name':' PRO 用户中心【humi-app-user】', 'url':'https://apis.360humi.com/humi-app-user/actuator/health'},
                {'name':' PRO 工业课堂【humi-app-community】', 'url':'https://apis.360humi.com/humi-app-community/actuator/health'},
                {'name':' PRO 认证中心【humi-app-security】', 'url':'https://apis.360humi.com/humi-app-security/actuator/health'}
            ]

book = xlwt.Workbook(encoding='utf-8')      #创建工作簿
sheet = book.add_sheet('sheet1')            #创建工作表格

#字体样式设置
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = '宋体'
font.height = 20 * 14  # 字体大小，12为字号，20为衡量单位
font.bold = True  # 黑体
style.font = font  # 设定样式
style.alignment = alignment
# 设置单元格宽度
sheet.col(0).width = 8300
sheet.col(1).width = 4000
sheet.col(2).width = 4500
sheet.col(3).width = 4500
sheet.col(4).width = 5000
sheet.col(5).width = 4000

sheet.write_merge(0, 0, 0, 5, str(time.strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日'))+'日报-后端服务检查结果', style)

sheet.write(1, 0, '服务名称', style)
sheet.write(1, 1, 'HTTP状态码', style)
sheet.write(1, 2, 'DNS解析时间', style)
sheet.write(1, 3, '建立连接时间', style)
sheet.write(1, 4, '平均下载速度', style)
sheet.write(1, 5, '服务状态', style)
n = 1
for item in serverList:
    n += 1
    print('\n**********' + item['name'] + '**********' + str(n))
    try:
        checkServer(sheet, item['name'], item['url'], n)
    except Exception as e:
        print(e)
        continue


book.save(str(time.strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日'))+str(time.time()) + '.xls')      #保存到test表格中