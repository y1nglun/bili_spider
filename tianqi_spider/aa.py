import re
import matplotlib.pyplot as plt
import csv

# 读取CSV文件并提取数据
with open('bannian.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # 读取表头
    data = list(reader)    # 读取数据

# 提取每个月份的数据
months = []
high_temps = []
low_temps = []
air_averages = []
air_worsts = []

for row in data[1:]:
    months.append(int(row[0]))
    high_temp = re.findall(r'\d+', row[1])[0]
    low_temp = re.findall(r'\d+', row[2])[0]
    high_temps.append(int(high_temp))
    low_temps.append(int(low_temp))
    air_averages.append(int(row[5]))
    air_worsts.append(int(row[6]))

# 创建柱状图和折线图
fig, ax1 = plt.subplots()

# 绘制温度图
ax1.set_xlabel('Month')
ax1.set_ylabel('Temperature (℃)')
ax1.plot(months, high_temps, color='red', marker='o', label='High Temp')
ax1.plot(months, low_temps, color='blue', marker='o', label='Low Temp')
ax1.legend(loc='upper left')

# 创建第二个坐标轴，绘制空气质量图
ax2 = ax1.twinx()
ax2.set_ylabel('Air Quality')
ax2.plot(months, air_averages, color='green', marker='o', label='Air Average')
ax2.plot(months, air_worsts, color='orange', marker='o', label='Air Worst')
ax2.legend(loc='upper right')

# 设置图表标题
plt.title('Weather Analysis (Jan-Jun 2023)')

# 展示图表
plt.show()
