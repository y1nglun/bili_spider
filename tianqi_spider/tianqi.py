import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

with open('weather_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Month', 'High', 'Low', 'Air_high', 'Air_low'])

    for mon in range(1, 13):
        month_str = str(mon).zfill(2)
        url = f'https://lishi.tianqi.com/mengzi/2022{month_str}.html'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        high = soup.select('.tian_two li')[0].select_one('.tian_twoa').get_text()
        low = soup.select('.tian_two li')[0].select('.tian_twoa')[1].get_text()
        air_best = soup.select('.tian_two li')[4].select('.tian_twoa')[0].get_text()
        air_low = soup.select('.tian_two li')[5].select('.tian_twoa')[0].get_text()

        writer.writerow([month_str, high, low, air_best, air_low])
