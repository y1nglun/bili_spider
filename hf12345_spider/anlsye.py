import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

df = pd.read_csv('scraped_data.csv')

df['Year'] = pd.to_datetime(df['Date'], format="%Y年%m月%d日").dt.year

yearly_counts = df.groupby('Year').size()

plt.figure(figsize=(8, 6))

yearly_counts.plot(kind='bar')
plt.xlabel('年份')
plt.ylabel('要问数量')
plt.title('每年发表食品安全要问数量分析')
plt.show()
