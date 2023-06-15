import csv
import matplotlib.pyplot as plt
from matplotlib import font_manager


gender_counts = {'男性': 0, '女性': 0, '未知': 0}

total_word_count = 0
font_path = 'C:/Windows/Fonts/STHUPO.TTF'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

with open('protect_eyes.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        gender = int(row['gender'])
        content = row['content']


        if gender == 1:
            gender_counts['男性'] += 1
        elif gender == -1:
            gender_counts['女性'] += 1
        else:
            gender_counts['未知'] += 1

        # 计算内容字数
        word_count = len(content.split())
        total_word_count += word_count


print('Gender Counts:')
for gender, count in gender_counts.items():
    print(f'{gender}: {count}')


average_word_count = total_word_count / len(gender_counts)
print(f'Average Word Count: {average_word_count}')


genders = list(gender_counts.keys())
counts = list(gender_counts.values())

plt.bar(genders, counts)
plt.xlabel('性别')
plt.ylabel('文章字数')
plt.title('性别与所发文章字数分析')
plt.show()
