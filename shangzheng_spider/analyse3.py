import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/msyh.ttc'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

categories = ['0~2000', '2000~3000', '3000~4000', '4000+']
category_counts = [0] * len(categories)

with open('index_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        index = float(row['Close'])

        if 0 <= index < 2000:
            category_counts[0] += 1
        elif 2000 <= index < 3000:
            category_counts[1] += 1
        elif 3000 <= index < 4000:
            category_counts[2] += 1
        elif index >= 4000:
            category_counts[3] += 1


plt.figure(figsize=(8, 6))
plt.pie(category_counts, labels=categories, autopct='%1.1f%%', startangle=90)
plt.title("指数分类占比", y=1.1)
plt.axis('equal')
plt.savefig('zhishu.png')
plt.show()
