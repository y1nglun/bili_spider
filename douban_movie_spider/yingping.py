import time

import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}
cookie = 'll="108288"; bid=Z_3vBiV0kFs; __yadk_uid=TMVLAENOBkftolAgRlNPIueGpWua0kX4; _vwo_uuid_v2=D28773AA2EE3F0E2F20E0ADE9004D9CD8|e568fb4ed1c269638799a6da4691ed0c; douban-fav-remind=1; dbcl2="186160890:EjnkiO9pknM"; push_noty_num=0; push_doumail_num=0; ct=y; __utmv=30149280.18616; ck=i5eL; ap_v=0,6.0; __utma=30149280.1241984296.1685431973.1686728135.1686790232.5; __utmc=30149280; __utmz=30149280.1686790232.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.2136563401.1685431973.1685431973.1686790283.2; __utmb=223695111.0.10.1686790283; __utmc=223695111; __utmz=223695111.1686790283.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1686790283%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utmb=30149280.4.10.1686790232; frodotk_db="ba9c278cf80809cb2fd476a6e8181d61"; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=24aa590f75720e57.1681197762..1686792112.undefined.'

data = []
for offset in range(0, 3220, 20):
    url = f'https://movie.douban.com/subject/32659890/reviews?start={offset}'
    print('scraping:', url)
    response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
    soup = BeautifulSoup(response.text, 'lxml')
    for item in soup.select('.review-list > div'):
        cid = item['data-cid']
        name = item.select_one('.name').get_text().strip()
        date = item.select_one('.main-meta').get_text().strip()
        print(cid, name, date)
        unfold_match = item.select_one('.unfold')
        if unfold_match:
            detail_url = f'https://movie.douban.com/j/review/{cid}/full'
            print('scraping:', detail_url)
            response = requests.get(detail_url, headers=headers).json()
            detail_html = response['html']
            soup = BeautifulSoup(detail_html, 'lxml')
            detail = soup.get_text().strip()
            data.append({'CID': cid, 'Name': name, 'Date': date, 'Detail': detail})
    time.sleep(1.5)

df = pd.DataFrame(data)
df.to_csv('reviews.csv', index=False)
