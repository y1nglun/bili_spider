import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/msyh.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

categories = ['-10%~-2%', '-2%~-1%', '-1%~0%', '0%~1%', '1%~2%', '2%~10%']
category_counts = [0] * len(categories)

with open('index_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        change = float(row['Zhangdiefu'].strip('%'))

        if -10 <= change < -2:
            category_counts[0] += 1
        elif -2 <= change < -1:
            category_counts[1] += 1
        elif -1 <= change < 0:
            category_counts[2] += 1
        elif 0 <= change < 1:
            category_counts[3] += 1
        elif 1 <= change < 2:
            category_counts[4] += 1
        elif 2 <= change <= 10:
            category_counts[5] += 1

plt.figure(figsize=(8, 6))
plt.pie(category_counts, labels=categories, autopct='%1.1f%%', startangle=90)
plt.title("涨跌幅度分类占比")
plt.axis('equal')
plt.savefig('zhangdiefu.png')
plt.show()
