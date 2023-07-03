import csv
import json
import time
import re
import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.weather.com.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

params = {
    '_': int(time.time() * 1000),
}

data_list = []  # 存储需要写入CSV的数据列表

for year in range(2022, 2024):
    # 发送GET请求获取页面内容
    response = requests.get(
        f'http://d1.weather.com.cn/calendar_new/{year}/101091001_{year}06.html',
        params=params,
        headers=headers,
        verify=False,
    )
    response.encoding = 'utf-8'

    # 使用正则表达式匹配并提取JSON数据
    json_match = re.search(r'fc40 = (.*)', response.text).group(1)
    json_data = json.loads(json_match)

    for item in json_data:
        # 提取所需的字段数据
        date = item['date']
        jiangyu = item['hgl']
        hmax = item['hmax']
        hmin = item['hmin']
        wk = item['wk']
        yl = item['yl']

        # 将数据添加到数据列表中
        data_list.append([date, jiangyu, hmax, hmin, wk, yl])

# 写入CSV文件
with open('weather_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入表头
    writer.writerow(['日期', '降雨概率', '最高气温', '最低气温', '星期', '节日'])

    # 写入数据列表
    writer.writerows(data_list)
