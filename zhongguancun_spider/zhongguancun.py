import time
import pymysql
import requests
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urljoin

connection = pymysql.connect(
    host="localhost",
    user="",
    password="",
)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
database_name = 'computer'
base_url = 'https://detail.zol.com.cn/'
create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
with connection.cursor() as cursor:
    cursor.execute(create_database_query)

# 切换到创建的数据库
connection.select_db(database_name)

# 创建表格
table_name = 'computer'
create_table_query = f'''
CREATE TABLE IF NOT EXISTS {table_name} (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255),
  pval_name VARCHAR(255),
  cao VARCHAR(255),
  year INT,
  month INT,
  price VARCHAR(255),
  neicun VARCHAR(255),
  cunchu VARCHAR(255),
  size VARCHAR(255),
  fenbian VARCHAR(255),
  weight VARCHAR(255),
  comment VARCHAR(255),
  score VARCHAR(255)
)
'''
with connection.cursor() as cursor:
    cursor.execute(create_table_query)

cursor = connection.cursor()
for page in range(1, 53):
    url = fr'https://detail.zol.com.cn/tablepc/{page}'
    print('scraping url:', url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for item in soup.select('.list-item'):
        title = item.select_one('h3').get_text().strip()
        pval = item.select_one('.pval a')
        if pval:
            pval_name = pval.get_text().strip()
        else:
            pval_name = ''
        cao_match = re.search(r'操作系统：(.+)', item.text)
        if cao_match:
            cao = cao_match.group(1).replace('\t', '')
        else:
            cao = ''
        price = item.select_one('.price-type').get_text()
        neicun_match = re.search(r'系统内存：(.+)', item.text)
        if neicun_match:
            neicun = neicun_match.group(1)
        else:
            neicun = ''
        cunchu_match = re.search(r'存储容量：(.+)', item.text)
        if cunchu_match:
            cunchu = cunchu_match.group(1)
        else:
            cunchu = ''
        size_match = re.search(r'屏幕尺寸：(.+)', item.text)
        if size_match:
            size = size_match.group(1)
        else:
            size = ''
        fenbian_match = re.search(r'屏幕分辨率：(.+)', item.text)
        if fenbian_match:
            fenbian = fenbian_match.group(1)
        else:
            fenbian = ''
        weight_match = re.search(r'产品重量：(.+)', item.text)
        if weight_match:
            weight = weight_match.group(1).split(' ')[0].strip()
        else:
            weight = ''
        comment_match = re.search(r'(.+)人点评', item.text)
        if comment_match:
            comment = comment_match.group(1)
        else:
            comment = ''
        score_item = item.select_one('.grade b')
        if score_item:
            score = score_item.get_text().strip()
        else:
            score = ''
        more_link = item.select_one('.more')
        if more_link and 'href' in more_link.attrs:
            link = more_link['href']
            res = requests.get(urljoin(base_url, link), headers=headers)
            s = BeautifulSoup(res.text, 'lxml')
            # date = s.select_one('.hover-edit-param').get_text().strip()
            # print(date)
            detail = s.select_one('.detailed-parameters')
            date_match = re.search(r'(\d{4})年(\d{1,2})月', detail.text)
            if date_match:
                year = date_match.group(1)
                month = date_match.group(2)
                print(year, month)
            else:
                year = ''
                month = ''
        else:
            link = ''
        query = "INSERT INTO computer (title, pval_name, cao, year, month, price, neicun, cunchu, size, fenbian, weight, comment, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (title, pval_name, cao, year, month, price, neicun, cunchu, size, fenbian, weight, comment, score)

        cursor.execute(query, values)

connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
