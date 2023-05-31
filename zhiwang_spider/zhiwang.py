from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

browser = webdriver.Chrome()
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
chrome_options.add_argument(user_agent)


def parse_index():
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fz14')))
    soup = BeautifulSoup(browser.page_source, 'lxml')
    items = soup.select('tr')
    print(items)
    for item in items:
        try:
            name = item.select_one('.fz14').text
            link = item.select_one('.fz14')['href']
            author = item.select_one('.author a').text
            source = item.select_one('.source a').text
            date = item.select_one('.date').text
            data = item.select_one('.data').text
            download = item.select_one('.operat a')['href']
            response = requests.get(link, headers=headers)
            print(response.text)
        except:
            continue


if __name__ == '__main__':
    browser.get('https://www.cnki.net/')
    wait = WebDriverWait(browser, 10)

    input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-input')))
    submit = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-btn')))

    input.send_keys('Hadoop')
    submit.click()
    parse_index()
