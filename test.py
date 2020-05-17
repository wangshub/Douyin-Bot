from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
browser.get('http://www.baidu.com')
input = browser.find_element(By.ID, 'kw')
input.send_keys('ipad')
time.sleep(1)
input.clear()
input.send_keys('MacBook pro')
button = browser.find_element(By.ID, 'su')
button.click()
time.sleep(5)
browser.quit()