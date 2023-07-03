import json
import csv
import requests
import re

cookies = {
    'gidinf': 'x099980109ee16c984751e404000608fc0a96c0796a9',
    '__bid_n': '1873a9ed99187516d04207',
    'SUV': '1680786396609852',
    '_muid_': '1680786396608966',
    'FPTOKEN': '22Y8wX0usRl9XSrc+fDnK5RcvbICAP5CSJc/N3BbLiKqFC04qzKVnR4aa98KK19Xp0q3eiod+FRM+BT2d3gzhLsvNWHM+/q8RdElyH2Fj5cWVF5lWs8HTLCS0hsTHI8mcrDxrgO+pht8rqcG5J5B0ZIL9+fnJF4FylP38qxIKOaqa4sURfhDHWU1hW65v5Qt4gd49vKLcAm8QJAzOyBViiQm20XJdCjYe1meUZJMhrZIAkHXhEdfx8f0A2qPk+VbP+AVVMH7xj+KuJQjd28Tfs8YrLbJbFctXKe9rmwVmX9dTJdCIfe+3+k3duZWlnu2d2u+a5aZY1amgaCc6q8fMneVDsBrkKcVCy77ARWvZCOethqOl0xBdbhO+M5xG+y2iG0rgdqbrgcFwpKLqEHXmw==|wNqabueqbgibtQI8DTBwdQEwaKvURuGHn+TPxwxVtuQ=|10|dd61d61ee01d7fb2d078dbe12c481fb1',
    'clt': '1687138165',
    'cld': '20230619092925',
    'reqtype': 'pc',
    'IPLOC': 'CN1100',
    't': '1687171398941',
}

headers = {
    'authority': 'q.stock.sohu.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': 'gidinf=x099980109ee16c984751e404000608fc0a96c0796a9; __bid_n=1873a9ed99187516d04207; SUV=1680786396609852; _muid_=1680786396608966; FPTOKEN=22Y8wX0usRl9XSrc+fDnK5RcvbICAP5CSJc/N3BbLiKqFC04qzKVnR4aa98KK19Xp0q3eiod+FRM+BT2d3gzhLsvNWHM+/q8RdElyH2Fj5cWVF5lWs8HTLCS0hsTHI8mcrDxrgO+pht8rqcG5J5B0ZIL9+fnJF4FylP38qxIKOaqa4sURfhDHWU1hW65v5Qt4gd49vKLcAm8QJAzOyBViiQm20XJdCjYe1meUZJMhrZIAkHXhEdfx8f0A2qPk+VbP+AVVMH7xj+KuJQjd28Tfs8YrLbJbFctXKe9rmwVmX9dTJdCIfe+3+k3duZWlnu2d2u+a5aZY1amgaCc6q8fMneVDsBrkKcVCy77ARWvZCOethqOl0xBdbhO+M5xG+y2iG0rgdqbrgcFwpKLqEHXmw==|wNqabueqbgibtQI8DTBwdQEwaKvURuGHn+TPxwxVtuQ=|10|dd61d61ee01d7fb2d078dbe12c481fb1; clt=1687138165; cld=20230619092925; reqtype=pc; IPLOC=CN1100; t=1687171398941',
    'referer': 'https://q.stock.sohu.com/zs/000001/lshq.shtml',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://q.stock.sohu.com/hisHq?code=zs_000001&start=20080101&end=20230619&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&r=0.8820606952635219&0.8691461043796889',
    cookies=cookies,
    headers=headers,
)
csv_file_path = "index_data.csv"

data = re.search(r'\((.*?)\)', response.text).group(1)
json_data = json.loads(data)
hq_list = json_data[0]['hq']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Date', 'Open', 'Close', 'Change', 'Zhangdiefu', 'Low', 'High', 'Succeed', 'Succeed Price'])

    for item in hq_list:
        date = item[0]
        open_index = item[1]
        close_index = item[2]
        change = item[3]
        zhangdiefu = item[4]
        low = item[5]
        high = item[6]
        succeed = item[7]
        succeed_price = item[8]
        print(date, open_index, close_index, change)
        writer.writerow([date, open_index, close_index, change, zhangdiefu, low, high, succeed, succeed_price])

print("数据已成功保存到CSV文件！")
