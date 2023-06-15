import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
data = pd.read_csv('protect_eyes.csv')
data['content'] = data['content'].fillna('')
text = ' '.join(data['content'])

seg_list = jieba.cut(text)

filtered_words = [word for word in seg_list if len(word) >= 2]

filtered_text = ' '.join(filtered_words)

wordcloud = WordCloud(font_path='C:/Windows/Fonts/STHUPO.TTF', width=800, height=400,
                      background_color='white').generate(filtered_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('关键词词云')
plt.show()
