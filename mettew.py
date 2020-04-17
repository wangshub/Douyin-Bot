from bs4 import BeautifulSoup
import requests

import xlsxwriter

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

base_url = 'http://www.mettew.com'
url = 'http://www.mettew.com/companies'
div_class_name = 'col-md-8 search_div'
all_url = []

response = requests.get(url)
# 内容
divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_=div_class_name)
for div in divs:
    for ul in div.find_all('ul'):
        temp_url = base_url + ul.li.a['href']
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





# workbook = xlsxwriter.Workbook('C:/Users/windows/Desktop/com.xlsx')
# worksheet = workbook.add_worksheet()
# for index, content in enumerate(names):
#     row = 'A' + str(index + 1)
#     row1 = 'B' + str(index + 1)
#     row2 = 'C' + str(index + 1)
#     row3 = 'D' + str(index + 1)
#     worksheet.write(row, content)
#     worksheet.write(row1, server[index])
#     worksheet.write(row2, phone[index])
#     worksheet.write(row3, email[index])
#
# workbook.close()
