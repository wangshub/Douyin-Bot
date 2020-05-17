from bs4 import BeautifulSoup
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# import time


def get_source():
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


def next_page(page_num):
    WAIT = WebDriverWait(browser, 10)   # 设置超时时长为10s
    try:
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.page-wrap > div > ul > li.page-item.active > button'), str(page_num)))
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):
    infos = soup.find_all(class_='video-item matrix')
    for info in infos:
        title = info.find('a').get('title')
        href = info.find('a').get('href')
        desc = info.find(class_='des hide').string.strip()
        views = info.find(class_='so-icon watch-num').text.strip()
        barrages = info.find(class_='so-icon hide').text.strip()
        date = info.find(class_='so-icon time').text.strip()
        up = info.find(class_='up-name').string.strip()
        print(f'爬取: {title} up主: {up} 观看次数: {views}')
        global n
        sheet.write(n, 0, title)
        sheet.write(n, 1, desc)
        sheet.write(n, 2, views)
        sheet.write(n, 3, barrages)
        sheet.write(n, 4, date)
        sheet.write(n, 5, up)
        sheet.write(n, 6, href)
        n += 1


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)   # 设置无界面爬虫
    browser.set_window_size(1400, 900)  # 设置全屏，注意把窗口设置太小的话可能导致有些button无法点击

    n = 1
    excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = excel.add_sheet('爱乐之城b站视频信息', cell_overwrite_ok=True)
    sheet.write(0, 0, '标题')
    sheet.write(0, 1, '描述')
    sheet.write(0, 2, '观看次数')
    sheet.write(0, 3, '弹幕数量')
    sheet.write(0, 4, '上传时间')
    sheet.write(0, 5, 'up主')
    sheet.write(0, 6, '视频链接')

    browser.get('https://bilibili.com')
    # 刷新一下，防止搜索button被登录弹框遮住
    # home = browser.find_element(By.CLASS_NAME, 'home')
    # home.click()
    browser.refresh()
    input = browser.find_element(By.CLASS_NAME, 'nav-search-keyword')
    button = browser.find_element(By.CLASS_NAME, 'nav-search-btn')
    input.send_keys('爱乐之城')
    button.click()
    all_h = browser.window_handles
    browser.switch_to.window(all_h[1])
    # total_btn = browser.find_element(By.CSS_SELECTOR, "#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.last > button")
    total_btn = browser.find_element(By.CSS_SELECTOR, "div.page-wrap > div > ul > li.page-item.last > button")
    total = int(total_btn.text)
    print(f'总页数: {total}')
    get_source()

    for i in range(2, total + 1):
        next_page(i)

    excel.save(u'爱乐之城b站视频信息.xls')

    browser.quit()
    print(f'共爬取{n-1}条信息')