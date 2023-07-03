import time

import requests
from bs4 import BeautifulSoup

import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
cookie = 'll="108288"; bid=Z_3vBiV0kFs; douban-fav-remind=1; dbcl2="186160890:EjnkiO9pknM"; push_noty_num=0; push_doumail_num=0; ct=y; __utmv=30149280.18616; __yadk_uid=jnngP53zU1kjVlEW0fFy53vD6oiYmn96; _vwo_uuid_v2=DEA5D9D49699F5AD472D715F3073AFF58|ef014ff15a65a92198f570bbdc045bce; ck=i5eL; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1686728117%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; frodotk_db="0804277070da5ab0180c7651528f1010"; __utma=30149280.1241984296.1685431973.1686537416.1686728135.4; __utmc=30149280; __utmz=30149280.1686728135.4.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=81379588.678443792.1686537416.1686539776.1686728135.3; __utmc=81379588; __utmz=81379588.1686728135.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=a9a398b8f1cf5781.1686537246.2.1686730121.1686539776.'
data = []


def gerHtml(url):
    response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
    print(response.status_code)
    return response.text


def parseHtml(html):
    soup = BeautifulSoup(html, 'lxml')
    for item in soup.select('.comment-item'):
        user = item.select_one('.comment-info a').get_text().strip()
        content = item.select_one('.comment-content').get_text().strip()
        times = item.select_one('.comment-time').get_text().strip()
        stars_element = item.select_one('.user-stars')
        stars = stars_element['title'] if stars_element else ''
        print(user, times)
        data.append({'User': user, 'Content': content, 'Time': times, 'Stars': stars})


def save():
    with open('jinxiandaishi.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['User', 'Content', 'Time','Stars']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    for offset in range(0, 60, 20):
        url = f'https://book.douban.com/subject/4162636/comments/?start={offset}&limit=20&status=P&sort=score'
        print('scraping', url)
        html = gerHtml(url)
        parseHtml(html)
        time.sleep(1.5)
    save()


main()
