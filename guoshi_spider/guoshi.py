import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'http://hprc.cssn.cn/wxzl/wxysl/lczf/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}


def parse_detail(link, title):
    # 构建详情页的完整链接
    detail_url = urljoin(url, link)
    # 发送请求获取详情页内容
    response = requests.get(detail_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # 使用CSS选择器定位到文章内容并提取文本
    content = soup.select_one('.TRS_Editor').get_text()
    # 将内容写入到以标题为文件名的文本文件中
    with open(f"{title}.txt", "w", encoding="utf-8") as file:
        file.write(content)


# 发送请求获取主页面内容
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

# 遍历需要爬取的年份范围
for year in range(2020, 2024):
    # 使用CSS选择器定位到对应年份的链接并获取链接地址
    link = soup.select_one(f'a[title="{year}年政府工作报告"]')['href']
    # 调用解析详情页函数，传入链接和标题参数
    parse_detail(link, f'{year}年政府工作报告')
