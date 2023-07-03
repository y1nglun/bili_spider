from bs4 import BeautifulSoup
import requests
import csv
import json

cookies = {
    'XSRF-TOKEN': '3b62d290-e0d4-4c15-8542-20321f8b743c',
    'cna': 'bdCrHGAC/FkCAd3cZuiGIm7/',
    'xlly_s': '1',
    'isg': 'BA0NWYRuVWAOhfFMigRg1RskHCmH6kG8tcKGOU-SoqQzRiz4FjlvjQeXsNoggFl0',
    'l': 'fBNLB3j7Nmrq2eR1BO5Iourza77T5IRb8rVzaNbMiIEGa1-ROEc6DNC19NOy5dtjgT5qTeKrip0J_dFXSVz38AkDBeYIobvIbXp68etzRyMc.',
    'tfstk': 'c1A1B7XmBlq_XnG0sGgeNDL-_YfAZIqC-Ase501moLnIP6Y1iZPPVUAWnk1Vkw1..',
}

headers = {
    'authority': 'search.damai.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': 'XSRF-TOKEN=3b62d290-e0d4-4c15-8542-20321f8b743c; cna=bdCrHGAC/FkCAd3cZuiGIm7/; xlly_s=1; isg=BA0NWYRuVWAOhfFMigRg1RskHCmH6kG8tcKGOU-SoqQzRiz4FjlvjQeXsNoggFl0; l=fBNLB3j7Nmrq2eR1BO5Iourza77T5IRb8rVzaNbMiIEGa1-ROEc6DNC19NOy5dtjgT5qTeKrip0J_dFXSVz38AkDBeYIobvIbXp68etzRyMc.; tfstk=c1A1B7XmBlq_XnG0sGgeNDL-_YfAZIqC-Ase501moLnIP6Y1iZPPVUAWnk1Vkw1..',
    'referer': 'https://search.damai.cn/search.html?keyword=%E4%BA%94%E6%9C%88%E5%A4%A9&spm=a2oeg.search_category.searchtxt.dsearchbtn2',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-xsrf-token': '3b62d290-e0d4-4c15-8542-20321f8b743c',
}

params = {
    'keyword': '五月天',
    'cty': '',
    'ctl': '',
    'sctl': '',
    'tsg': '0',
    'st': '',
    'et': '',
    'order': '0',
    'pageSize': '30',
    'currPage': '1',
    'tn': '',
}

all = []


def getJson(url):
    try:
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        print('response status_code:', response.status_code)
        return response.json()
    except:
        return ''


def parseJson(jsons):
    for item in jsons['pageData']['resultData']:
        name_html = item['name']
        soup = BeautifulSoup(name_html, 'lxml')
        name = soup.get_text().strip()
        venuecity = item['venuecity']
        venue = item['venue']
        price_str = item['price_str']

        single = [name, venuecity, venue, price_str]
        all.append(single)


def printList(num):
    print("{:^4}{:^10}{:^5}{:^8}".format("名字", "城市", "地点", "价格"))
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
    url = 'https://search.damai.cn/searchajax.html'
    jsons = getJson(url)
    parseJson(jsons)
    printList(len(all))
    filename = input("请输入要保存的文件名（不带扩展名）：")
    path = input("请输入要保存的文件路径：")
    writeCSV(filename, path)
    writeJSON(filename, path)


main()
