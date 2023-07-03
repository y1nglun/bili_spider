import requests
from bs4 import BeautifulSoup
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
        print('response status_code:', response.status_code)
        return response.text
    except:
        return ''


def parseHTML(html):
    soup = BeautifulSoup(html, 'lxml')
    skip_first_row = True

    for item in soup.select('.mod_table')[0].select('.md_tr'):
        if skip_first_row:
            skip_first_row = False
            continue
        time = item.select('.md_td')[0].get_text().strip()
        place = item.select('.md_td')[1].get_text().strip()
        single = [time, place]
        all.append(single)


def printList(num):
    print("{:^4}{:^10}".format("时间", "地点"))
    for i in range(num):
        u = all[i]
        print("{:^4}{:^10}".format(u[0], u[1]))


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
    url = 'https://www.maigoo.com/news/653208.html'
    html = getHTMLText(url)
    parseHTML(html)
    printList(len(all))
    filename = input("请输入要保存的文件名（不带扩展名）：")
    path = input("请输入要保存的文件路径：")
    writeCSV(filename, path)
    writeJSON(filename, path)


main()
