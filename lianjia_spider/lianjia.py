import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    data = []
    for index, item in enumerate(soup.select('.sellListContent li'), 1 + (page - 1) * 30):
        title = item.select_one('.title a').get_text()
        detail = item.select_one('.houseInfo').get_text()
        total_price = item.select_one('.totalPrice span').get_text()
        price = item.select_one('.unitPrice span').get_text()

        print(title, detail, total_price, price)

        data.append({
            '序号': index,
            '标题': title,
            '房屋详细信息': detail,
            '总价': total_price,
            '单价': price
        })

    return data


def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)


file_name = "data"

results = []
for page in range(1, 51):
    url = f'https://zz.lianjia.com/ershoufang/pg{page}/'
    response = requests.get(url, headers=headers)
    print('status code:', response.status_code)
    page_data = parse(response.text)
    results.extend(page_data)

# 获取当前工作目录
current_dir = os.getcwd()
# 构建文件路径
excel_file_path = os.path.join(current_dir, f"{file_name}.xlsx")

save_to_excel(results, excel_file_path)

print("数据保存成功！")
