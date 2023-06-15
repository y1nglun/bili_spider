import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

data = pd.read_csv('weather_data.csv')
data['High'] = data['High'].str.replace('℃', '')
data['Low'] = data['Low'].str.replace('℃', '')

months = data['Month']
high_temps = data['High'].astype(int)
low_temps = data['Low'].astype(int)
air_high = data['Air_high']
air_low = data['Air_low']

avg_temps = (high_temps + low_temps) / 2
avg_air_quality = (air_high + air_low) / 2

plt.plot(months, avg_temps, label='平均温度')
plt.xlabel('月份')
plt.ylabel('温度 (°C)')
plt.title('蒙自市2022年平均温度趋势')
plt.legend()
plt.show()

plt.plot(months, avg_air_quality, label='平均空气质量')
plt.xlabel('月份')
plt.ylabel('空气质量')
plt.title('蒙自市2022年平均空气质量趋势')
plt.legend()
plt.show()
