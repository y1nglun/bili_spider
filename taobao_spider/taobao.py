import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
from bs4 import BeautifulSoup

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
chrome_options.add_argument('User-Agent=' + user_agent)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=chrome_options)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
})
browser.set_window_size(1400, 900)

url = 'https://www.taobao.com'

wait = WebDriverWait(browser, 10)


def parse_index():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    soup = BeautifulSoup(browser.page_source, 'lxml')
    items = soup.select('#mainsrp-itemlist .items .item')
    for item in items:
        title = item.select_one('.title').text
        print(title)


"""
首次登陆,获取cookie
"""


def get_cookie():
    browser.get('https://login.taobao.com')
    time.sleep(10)
    cookies = browser.get_cookies()
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)


with open('cookies.pkl', 'rb') as file:
    loaded_cookies = pickle.load(file)
browser.get(url)
for cookie in loaded_cookies:
    browser.add_cookie(cookie)
browser.refresh()
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
submit = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-search')))
input.send_keys('jk')
submit.click()
parse_index()
