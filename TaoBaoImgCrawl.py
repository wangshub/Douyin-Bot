import selenium
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import getpass
from selenium.webdriver.common.action_chains import ActionChains


def login():
    try:
        login_by_pass = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')))
        login_by_pass.click()
        username = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1')))
        password = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1')))
        submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SubmitStatic')))
        # str1 = input('username: ')
        # str2 = getpass.getpass('password: ')
        username.send_keys('15210434997')
        password.send_keys('ll8023')
        # 保证滑块出现
        time.sleep(1)
        while True:
            slide = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1_n1z')))
            # 定义鼠标拖放动作
            ActionChains(browser).drag_and_drop_by_offset(slide, 400, 0).perform()
            # 等待认证成功
            time.sleep(2)
            text = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text')))
            if text.text == '验证通过':
                break
            else:   # 验证失败时刷新，重新获取滑块
                print('s')
                refresh_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nocaptcha > div.errloading > span.nc-lang-cnt > a')))
                refresh_btn.click()
        submit.click()
    except TimeoutException:
        login()


if __name__ == "__main__":
    chromedriver="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    options = Options()
    # options.add_argument('--proxy-server=127.0.0.1:8080')
    browser = selenium.webdriver.Chrome(options=options,executable_path=chromedriver)
    WAIT = WebDriverWait(browser, 10)
    browser.maximize_window()
    browser.get('https://taobao.com')

    logig_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.col-right > div.tbh-member.J_Module > div > div.member-ft > div.member-logout.J_MemberLogout > a.btn-login.ml1.tb-bg.weight')))
    logig_btn.click()

    all_h = browser.window_handles
    browser.switch_to.window(all_h[-1])

    login()

    time.sleep(5)
    browser.quit()