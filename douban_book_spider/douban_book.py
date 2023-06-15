import time

import requests
from bs4 import BeautifulSoup
import re
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
cookie = 'll="108288"; bid=Z_3vBiV0kFs; douban-fav-remind=1; dbcl2="186160890:EjnkiO9pknM"; push_noty_num=0; push_doumail_num=0; ct=y; __utmv=30149280.18616; ck=i5eL; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1686537246%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DZ3N-ab0hX-NoxnnKdtzCljlilh_H8UuuYYdQ5B6mXlYr-hp1gnbfueJ3y1bEvWGP%26wd%3D%26eqid%3Db689b504000023300000000264868418%22%5D; _pk_ses.100001.3ac3=*; __yadk_uid=jnngP53zU1kjVlEW0fFy53vD6oiYmn96; _vwo_uuid_v2=DEA5D9D49699F5AD472D715F3073AFF58|ef014ff15a65a92198f570bbdc045bce; __utma=30149280.1241984296.1685431973.1686304869.1686537416.3; __utmc=30149280; __utmz=30149280.1686537416.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.678443792.1686537416.1686537416.1686537416.1; __utmc=81379588; __utmz=81379588.1686537416.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; frodotk_db="73a2fd0d0bbe46275ae8f727233ad275"; _pk_id.100001.3ac3=a9a398b8f1cf5781.1686537246.1.1686538537.1686537246.; __utmt=1; __utmb=30149280.13.10.1686537416'

with open('douban_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Author', 'Link', 'Score', 'Introduce'])

    for page in range(0, 300, 25):
        url = f'https://www.douban.com/doulist/139873963/?start={page}&sort=seq&playable=0&sub_type='
        print('scraping url:', url)
        response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml')
        for item in soup.select('.doulist-subject'):
            title = item.select_one('.title a').get_text().strip()
            link = item.select_one('.title a')['href']
            author_match = re.search(r'作者: (.+)', item.text)
            if author_match:
                author = author_match.group(1)
            score = item.select_one('.rating_nums').get_text().strip()
            response = requests.get(link, headers=headers, cookies={'Cookie': cookie})
            print('scraping url:', link)
            soup = BeautifulSoup(response.text, 'lxml')
            introduce_element = soup.select_one('.intro p')
            if introduce_element:
                introduce = introduce_element.get_text().strip()
            else:
                introduce = ""

            writer.writerow([title, author, link, score, introduce])
            time.sleep(1.5)
