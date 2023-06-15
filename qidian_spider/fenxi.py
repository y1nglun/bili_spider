import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/simhei.ttf'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

df = pd.read_csv('data.csv')


top_10 = df.sort_values(by='月票', ascending=False).head(10)


book_names = top_10['书名']
monthly_tickets = top_10['月票']


plt.bar(book_names, monthly_tickets)
plt.xlabel('书名')
plt.ylabel('月票')
plt.title('排名前十图书的月票')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
