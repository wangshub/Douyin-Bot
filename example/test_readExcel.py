import xlrd
import random
#打开excel文件
data=xlrd.open_workbook('../reply/keyword.xlsx')
#获取第一张工作表（通过索引的方式）
table=data.sheets()[0]
#data_list用来存放数据
data_list=[]
#将table中第一行的数据读取并添加到data_list中
data_list.extend(table.col_values(0))
#打印出第一行的全部数据
for item in data_list:
    print(item)


