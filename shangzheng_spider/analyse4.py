import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/msyh.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()
continuous_up = 0
continuous_down = 0
discontinuous = 0
previous_change = None


with open('index_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        change = float(row['Change'])

        if previous_change is None:
            previous_change = change
        elif change > 0:
            if previous_change > 0:
                continuous_up += 1
            else:
                discontinuous += 1
        elif change < 0:
            if previous_change < 0:
                continuous_down += 1
            else:
                discontinuous += 1

        previous_change = change


labels = ['连续上涨', '连续下跌', '上涨或下跌不连续']
sizes = [continuous_up, continuous_down, discontinuous]
colors = ['#FFD700', '#FF4500', '#00BFFF']
explode = (0.1, 0, 0)

plt.figure(figsize=(12, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title("涨跌情况统计")
plt.axis('equal')
plt.savefig('continuous.png')
plt.show()
