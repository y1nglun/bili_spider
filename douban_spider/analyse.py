import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

# 读取json文件数据
data = pd.read_json('output.json')

# 电影评分分布 - 柱状图
plt.figure(figsize=(10, 6))
sns.histplot(data=data, x='score', bins=10, kde=True)
plt.xlabel('评分')
plt.ylabel('数量')
plt.title('电影评分分布')
plt.savefig('score_distribution.png')  # 保存柱状图
plt.show()

# 国家/地区分布 - 饼图
country_counts = data['country'].value_counts().head(10)
plt.figure(figsize=(8, 8))
plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%')
plt.title('前10个国家/地区分布')
plt.savefig('country_distribution.png')  # 保存饼图
plt.show()

# 评论时间趋势 - 折线图
data['comment_time'] = pd.to_datetime(data['comment_time'].astype(str).str.strip())
monthly_counts = data['comment_time'].dt.to_period('M').value_counts().sort_index()
plt.figure(figsize=(12, 6))
monthly_counts.plot(marker='o')
plt.xlabel('月份')
plt.ylabel('评论数量')
plt.title('评论时间趋势')
plt.xticks(rotation=45)
plt.savefig('comment_time_trend.png')  # 保存折线图
plt.show()

# 计算电影评分与评论数量的相关系数
correlation = data['score'].corr(data['comment'].str.len())

print("电影评分与评论数量的相关系数：", correlation)

# 计算各个国家/地区的电影评分平均值
average_ratings = data.groupby('country')['score'].mean()

print("各个国家/地区的电影评分平均值：")
print(average_ratings)
