import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

data = pd.read_csv('relitemp.csv', encoding='utf-8')

cities = data['name']
temperature_ranges = data['weather'].str.extract(r'(\d+) ~ (\d+)℃', expand=True).astype(int)
temperature_ranges.set_index(cities, inplace=True)

plt.figure(figsize=(10, 6))
font_path = 'C:/Windows/Fonts/STHUPO.TTF'
font = FontProperties(fname=font_path)
sns.set(font=font.get_name())
sns.heatmap(temperature_ranges, annot=True, cmap='coolwarm', cbar=True)

plt.xlabel('城市')
plt.ylabel('温度范围 (°C)')
plt.title('蒙自是城市温度热力图')

plt.xticks(rotation=45)

plt.show()
