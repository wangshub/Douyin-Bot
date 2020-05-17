from bs4 import BeautifulSoup
import requests
import json
import xlsxwriter

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Referer': 'http://epub.cnipa.gov.cn/patentoutline.action',
    'Host': 'epub.cnipa.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://epub.cnipa.gov.cn',
    'Cookie':'wIlwQR28aVgb80S=7D0gwwR2f5v2lhrZtdEIE8J78Hrn0KT_Fcdh.PZVmUE4uEYEbknDPIvY18yqAtfN; _gscu_2075282647=8872905527n27g14; _gscu_1670725265=88729139uldnzb19; _trs_uv=k9upgs08_4030_blqv; _va_ref=%5B%22%22%2C%22%22%2C1588731183%2C%22http%3A%2F%2Fwww.sipo.gov.cn%2F%22%5D; _va_id=f9a1ef168eb07ffc.1588731183.1.1588731378.1588731183.; WEB=20111132; JSESSIONID=C1E9743E61433645446D5121F42AEA4E; _gscbrs_2075282647=1; Hm_lvt_06635991e58cd892f536626ef17b3348=1588729140,1589184534; Hm_lpvt_06635991e58cd892f536626ef17b3348=1589184534; _gscbrs_1670725265=1; wIlwQR28aVgb80T=4FUCG6CZBQmr8gXKXI_0uLpqOvBW0aBQDvXhZHJApukXwEftuxVw66xZ5mXj0TUfiMNcF7XC.mukBDvEwVoyQ7lM_rZ_ey3V.GtFASK3OHvk7YXKxHAm2uE2arFBoivzuD2nFM84KwSFh0FeO.ThBeRzqwC9px.XBk7_b5OkQWLuhO4O8yjoKYXwbXCaitsXYfRBfvcH9CGB1izu9DA0B1CvggconMuBa6KaNpIREbIlSAKfk19L1eeLCg0Bgeo3K7IH42XAthQtj206viSaSv5uhAm0ZOdT5hvL_HBWtlVZxTixYr63l7.ZUp1eWGl6n3QRAbFiSs1tiXdatxQh.FznDdjUvhiX6MpIbBKh_kg2zdsL0hHXaeV0bB7hccMgaoKL'
}

postUrl = 'http://epub.cnipa.gov.cn/patentoutline.action'
parms = {
    'showType': 1,
    'strSources': 'pip',
    'strWhere': 'PA,IN,AGC,AGT+="%数据可视化%" or PAA,TI,ABH+="数据可视化"',
    'numSortMethod': 4,
    'strLicenseCode': '',
    'numIp': 0,
    'numIpc': '',
    'numIg': 0,
    'numIgc': '',
    'numIgd': '',
    'numUg': 0,
    'numUgc': 0,
    'numUgd': '',
    'numDg': 0,
    'numDgc': '',
    'pageSize': 10,
    'pageNow': 1
}
div_class_name = 'w790 right'
all_url = []

response = requests.post(url=postUrl, data=json.dumps(parms), headers=headers)
# 内容
divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
for div in divs:

    for item_div in div.find_all('cp_linr'):
        title = item_div.h1.string
        print(title)
        for ul in item_div.find_all('ul'):
            temp_url = ul.li.a['href']
            # if(temp_url == 'http://www.mettew.com/companies/2325'):
            print(ul.li.a.string + ' ' + temp_url)
            all_url.append(temp_url)

json_content = {}
for c_url in all_url:

    dict_company_name = {}
    dict_main_comment = {}
    dict_item_content = {}
    list_item_content = []

    company_div_class = 'nav_area_content'
    response = requests.get(c_url)
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=company_div_class)
    for div in divs:
        company_name = div.strong.string
        dict_company_name={'companyName': company_name}

    comments_div_class = 'comments_left pull-left'
    response = requests.get(c_url)
    beaut = BeautifulSoup(response.text, 'lxml')
    divs = beaut.find_all('div', class_=comments_div_class)
    for div in divs:
        main_comment = div.h4.string
        dict_main_comment = {'mainComment': main_comment}

    divs = beaut.find_all('div', class_='commentType')
    for div in divs:
        item_up_or_down = {}
        item_comment = {}
        item_date = {}
        item_re_comment = []
        item_re_comment_dict = {}

        item_divs = div.find_all('div')
        for item_div in item_divs:
            if item_div.attrs:
                item_div_class = ' '.join(item_div['class'])

                if 'comment_icon pull-left' == item_div_class:
                    if 'fa-thumbs-up' in item_div.i['class']:
                        up_or_down = 'up'
                    if 'fa-thumbs-down' in item_div.i['class']:
                        up_or_down = 'down'
                    dict_up_or_down = {"itemUpOrDown": up_or_down}

                if 'comment_txt pull-left' == item_div_class:
                    item_comment = {'itemComment': item_div.p.string}
                    item_date = {'itemDate': item_div.div.div.text}

                if 'comment_child' == item_div_class:
                    re_comment = {'reComment': item_div.p.string}
                    re_comment_date = {'reCommentDate': item_div.div.div.text}
                    re_comment.update(re_comment_date)

                    item_re_comment.append(re_comment)
                    # print(str(item_re_comment))

        item_re_comment_dict = {"itemReComment": item_re_comment}

        dict_up_or_down.update(item_comment)
        dict_up_or_down.update(item_date)
        dict_up_or_down.update(item_re_comment_dict)
        list_item_content.append(dict_up_or_down)
        # print(str(list_item_content))

    dict_item_content = {'itemContent': list_item_content}
    dict_company_name.update(dict_main_comment)
    dict_company_name.update(dict_item_content)
    print(str(dict_company_name))

