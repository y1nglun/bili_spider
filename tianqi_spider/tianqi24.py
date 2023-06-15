import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

with open('jiangyu.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Month', 'Jiangyuliang'])

    for mon in range(1, 13):
        month_str = str(mon).zfill(2)
        url = f'https://www.tianqi24.com/mengzi/history2022{month_str}.html'

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        jiangyuliang = soup.select('.mainArt section')[1].select('table tr')[1].select('td')[3].select_one(
            'span').get_text()
        writer.writerow([month_str, jiangyuliang])
