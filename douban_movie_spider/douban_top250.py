import requests
from bs4 import BeautifulSoup
import re
import csv
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

all = []


def getHTMLText(url):
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        return response.text
    except:
        return ''


def parseHTML(html):
    soup = BeautifulSoup(html, 'lxml')
    for item in soup.select('.grid_view .item'):
        title = item.select_one('.title').get_text().strip()
        daoyan_match = re.search('导演:\s+(\S+)', item.text)
        if daoyan_match:
            daoyan = daoyan_match.group(1)
        actor_match = re.search('主演:\s+(\S+)', item.text)
        if actor_match:
            actor = actor_match.group(1)
        score = item.select_one('.rating_num').get_text().strip()
        single = [title, daoyan, actor, score]
        all.append(single)


def printList(num):
    print("{:^4}{:^10}{:^5}{:^8}".format("名字", "导演", "主演", "评分"))
    for i in range(num):
        u = all[i]
        print("{:^4}{:^10}{:^5}{:^8}".format(u[0], u[1], u[2], u[3]))


def writeCSV(filename, path):
    with open(f'{path}/{filename}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["名字", "城市", "地点", "价格"])
        for row in all:
            writer.writerow(row)


def writeJSON(filename, path):
    with open(f'{path}/{filename}.json', 'w', encoding='utf-8') as file:
        json.dump(all, file, ensure_ascii=False, indent=4)


def main():
    url = 'https://movie.douban.com/top250?start=0'
    html = getHTMLText(url)
    parseHTML(html)
    printList(len(all))
    filename = input("请输入要保存的文件名（不带扩展名）：")
    path = input("请输入要保存的文件路径：")
    writeCSV(filename, path)
    writeJSON(filename, path)


main()
