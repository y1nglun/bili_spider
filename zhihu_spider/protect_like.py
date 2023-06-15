import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

data = pd.read_csv('protect_eyes.csv')

data['content'] = data['content'].fillna('')

data['Content_length'] = data['content'].apply(lambda x: len(x))

grouped_data = data.groupby(data['Content_length'] // 100 * 100)['like'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x=grouped_data['Content_length'], y=grouped_data['like'], color='skyblue')
plt.xlabel('文本字数')
plt.ylabel('平均点赞数量')
plt.title('点赞数量与文本字数关系')
plt.xticks(rotation=45)
plt.show()
