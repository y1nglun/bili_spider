import time
import re
import requests
from bs4 import BeautifulSoup
import csv
import jieba
from jieba.analyse import extract_tags
from wordcloud import WordCloud
import matplotlib.pyplot as plt

url = 'https://tech.hexun.com/2014/home/js/1moredata.js?'  # 数据请求的URL
params = {
    't': round(time.time() * 1000)  # 添加时间戳参数
}

headers = {
    # 设置请求头信息
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Cookie': 'ASL=19514,0000l,72f6408e; ADVC=3be646509143ca; ADVS=3be646509143ca; hxck_cd_sourceteacher=sR%2FuPcnSSZVIdShwHag3RAnrY9aauRbMjEnRBtq%2FNF1ooDP7obDVPgaQGWxsj76JqbJObjTyc6HyVvH5T5AJRP%2BDTUa9Lv110QVpbjB8cMWFpFirO92HUlW35USEgz7nShZJgmKTKnspODGDZIdg1vA%2BNG1apmukjkSj2T60Sac%3D; appToken=pc%2Cother%2Cchrome%2ChxAppSignId78673807503032941686021330413%2CPCDUAN; HexunTrack=SID=20230606111530146aea9e58621734f5ea35a3fbf16d33932&CITY=0&TOWN=0; ADHOC_MEMBERSHIP_CLIENT_ID1.0=44e601f1-b988-498a-3c17-935946620749; hexun_popuped=2023-06-06; hxck_cd_channel_order_mark1=tKK6EMkJ7JK75WOJ%2FqluxbbMrhZQZtn9if6%2FTggkwv1usWuXF1z7QXE0I2SwKUmrGjmkGyBOcl7z4p5%2Bu0H0TeTOCVoXLs17wi9XY5pWYLGeQZNbbiet0tv9%2BUlSFfta',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://tech.hexun.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

# 发送GET请求获取数据
response = requests.get(url, params=params, headers=headers)
data = response.text

start_index = data.find("TradeTab_JsonData=")  # 找到起始位置
content = data[start_index + len("TradeTab_JsonData="):].strip(";")  # 截取内容

title_match = re.findall(r"title:'(.*?)'", content)  # 使用正则表达式匹配标题
title_link_match = re.findall(r"titleLink:'(.*?)'", content)  # 使用正则表达式匹配链接
result = []

# 将匹配到的标题和链接存储为字典，并添加到列表中
for title, link in zip(title_match, title_link_match):
    item = {'title': title, 'link': link}
    result.append(item)

print(result)

csv_file = 'output.csv'  # CSV文件路径

# 使用CSV模块将列表数据写入CSV文件
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])  # 写入表头
    for item in result:
        writer.writerow([item['title'], item['link']])

news_text = ''

# 遍历结果列表，发送请求获取新闻内容，并将内容拼接到news_text中
for item in result:
    res = requests.get(item['link'], headers=headers, verify=False)
    for encoding in ['utf-8', 'gbk', 'gb2312']:
        try:
            content = res.content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if content is not None:
        soup = BeautifulSoup(content, 'lxml')
        text = soup.select('.art_contextBox')[0]
        news_text += text.get_text()
    else:
        print("无法解码文本数据")

clean_text = re.sub(r'\s+|\d+|[^\u4e00-\u9fa5a-zA-Z]', '', news_text)  # 清理文本
seg_list = jieba.lcut(clean_text)  # 使用jieba进行分词
keywords = extract_tags(clean_text, topK=5)  # 提取关键词
ci = ' '.join(keywords)

# 生成词云图
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(ci)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
