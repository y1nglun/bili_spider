import requests
from bs4 import BeautifulSoup
import csv
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}


def getHTML(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    print(response.status_code)
    return response.text


def parseHTML(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select_one('.con_article').get_text().strip()
    content_match = re.search(r'目前世界人口排名(.*?)人口', content)
    if content_match:
        text = content_match.group(1)
    pattern = r'第(\w+)名:(.*?)、([\d.]+)亿'
    matches = re.findall(pattern, text)

    with open('population_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['排名', '国家', '人口'])

        for match in matches:
            rank = match[0]
            country = match[1]
            population = match[2] + "亿"
            writer.writerow([rank, country, population])


def main():
    url = 'http://www.yiwenmi.cn/redianzixun/78280.html'
    html = getHTML(url)
    parseHTML(html)


main()
