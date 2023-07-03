import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

# 读取Excel表格数据
df = pd.read_excel('movies.xlsx')

# 查看数据概览
print(df.head())

# 统计年份分布
year_counts = df['年份'].value_counts().sort_index()

# 创建年份分布折线图
plt.plot(year_counts.index, year_counts.values)
plt.xlabel('年份')
plt.ylabel('电影数量')
plt.title('电影年份分布')

# 显示图表
plt.show()
