import json
import pandas
import requests
import time

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


url_request = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'  # network -> headers中显示的请求链接


def get_lagou(job_position, job_address):
    job_info = []
    # url = 'https://www.lagou.com/jobs/positionAjax.json?'
    url_html = 'https://www.lagou.com/jobs/list_' + job_position + '?labelWords=&fromSearch=true&suginput='  # 网页显示访问链接

    # 表示 页码 1-50页
    for i in range(1, 50):
        params = {
            'city': job_address,
            'first': 'true' if i == 1 else 'false',
            'pn': i,
            'kd': job_position
        }

        # 创建一个session对象
        s = requests.Session()
        # 发送请求，获得cookies
        s.get(url_html, headers=headers, data=params, timeout=4)
        cookie = s.cookies

        res = s.post(url_request, data=params, headers=headers, cookies=cookie, timeout=4)  # 注意分析网页数据获取格式
        res.encoding = res.apparent_encoding
        text = json.loads(res.text)

        for j in range(15):  # 每页数据只有1条
            info = text['content']['positionResult']['result'][j]

            company_full_name = info["companyFullName"]
            position_name = info["positionName"]
            salary = info["salary"]
            company_size = info["companySize"]
            skill_lables = info["skillLables"]
            create_time = info["createTime"]
            district = info["district"]
            station_name = info["stationname"]

            print("数据爬取成功：" + company_full_name + " " + position_name + " " + salary + " " + str(skill_lables) + " " + create_time)
            job_info.append(text['content']['positionResult']['result'][j])  # 职位信息具体的json存放位置

    print("------------------")
    print("数据爬取结束，正在生成excel文档......")
    df = pandas.DataFrame(job_info)  # 利用pandas将列表表格化
    now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())  # 以系统当前时间将爬取职位信息存放至本地csv文件
    df.to_csv(now + '.csv', encoding='gb18030')  # 将表格化数据永久化存储到本地csv文件
    print("生成成功！")


if __name__ == '__main__':
    address = input('请输入工作地点:>')
    job = input('请输入职位:>')
    get_lagou(job, address)