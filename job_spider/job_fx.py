import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import csv
from wordcloud import WordCloud

font_path = 'C:/Windows/Fonts/msyh.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

df = pd.read_csv('cleaned_job_data.csv')

df[['薪资最低', '薪资最高']] = df['薪资'].str.split('-', expand=True)

df['薪资最低'] = df['薪资最低'].str.extract('(\d+)', expand=False).astype(int)
df['薪资最高'] = df['薪资最高'].str.extract('(\d+)', expand=False).astype(int)

df['薪资平均'] = (df['薪资最低'] + df['薪资最高']) / 2
df['薪资平均'] = df['薪资平均'].astype(str) + 'K'

salary_avg_counts = df['薪资平均'].value_counts().sort_index()

plt.figure(figsize=(8, 8))
salary_avg_counts.plot(kind='pie', autopct='%1.1f%%')
plt.axis('equal')
plt.title('薪资范围平均值分布')
plt.show()

df = pd.read_csv('cleaned_job_data.csv')


company_counts = df['公司名称'].value_counts().nlargest(10)


plt.figure(figsize=(12, 10))
company_counts.plot(kind='bar')
plt.xlabel('公司名称')
plt.ylabel('出现次数')
plt.title('热门公司名称统计')
plt.show()

with open('cleaned_job_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    detailed_info = [row['详细信息'] for row in reader]


text = ' '.join(detailed_info)


wordcloud = WordCloud(background_color='white', font_path='C:/Windows/Fonts/msyh.ttc').generate(text)


plt.figure(figsize=(8, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
