import requests
import csv
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

# 创建CSV文件并写入表头
with open('bannian.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['High', 'Low', 'Max High', 'Max Low', 'Air Average', 'Air Best', 'Air Low'])

    for mon in range(1, 7):
        month_str = str(mon).zfill(2)
        url = f'https://lishi.tianqi.com/mengzi/2023{month_str}.html'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        high = soup.select('.tian_two li')[0].select_one('.tian_twoa').get_text()
        low = soup.select('.tian_two li')[0].select('.tian_twoa')[1].get_text()
        max_high = soup.select('.tian_two li')[1].select_one('.tian_twoa').get_text()
        max_low = soup.select('.tian_two li')[2].select_one('.tian_twoa').get_text()
        air_av = soup.select('.tian_two li')[3].select_one('.tian_twoa').get_text()
        air_best = soup.select('.tian_two li')[4].select('.tian_twoa')[0].get_text()
        air_low = soup.select('.tian_two li')[5].select('.tian_twoa')[0].get_text()

        writer.writerow([high, low, max_high, max_low, air_av, air_best, air_low])
