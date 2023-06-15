import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}
with open('relitemp.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'weather'])
    url = 'https://www.tianqi.com/honghe/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for item in soup.select('.mainWeather ul li'):
        try:
            name = item.select_one('a h5').get_text()
            weather = item.select_one('a p').get_text()
            writer.writerow([name, weather])
        except:
            pass
