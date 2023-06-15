import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('output.csv')

# 提取"name"列的数据并转换为字符串
names = df['Name'].astype(str).tolist()

# 将列表转换为以空格分隔的字符串
text = ' '.join(names)

# 创建WordCloud对象
wordcloud = WordCloud(width=800, height=400, background_color='white',
                      font_path='C:/Windows/Fonts/STHUPO.TTF').generate(text)

# 绘制词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
