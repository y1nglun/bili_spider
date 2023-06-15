import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

data = pd.read_csv('jiangyu.csv', encoding='utf-8')

months = data['Month']
rainfall = data['Jiangyuliang'].str.replace('(mm)', '').astype(float)

plt.plot(months, rainfall, marker='o')

plt.xlabel('月份')
plt.ylabel('降雨量 (mm)')
plt.title('蒙自市2022年月降雨量')

plt.show()
