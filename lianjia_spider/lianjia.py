import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    output = ""
    for index, item in enumerate(soup.select('.sellListContent li'), 1 + (page - 1) * 30):
        title = item.select_one('.title a').get_text()
        detail = item.select_one('.houseInfo').get_text()
        total_price = item.select_one('.totalPrice span').get_text()
        price = item.select_one('.unitPrice span').get_text()

        output += f"[序号] {index}\n"
        output += f"[标题] {title}\n"
        output += f"[房屋详细信息] {detail}\n"
        output += f"总价：{total_price}\n"
        output += f"单价：{price}\n"
        output += "\n"

        print(output)

    with open("output.txt", "a", encoding="utf-8") as file:
        file.write(output)


for page in range(1, 101):
    url = f'https://zz.lianjia.com/ershoufang/pg{page}/'
    response = requests.get(url, headers=headers)
    parse(response.text)
