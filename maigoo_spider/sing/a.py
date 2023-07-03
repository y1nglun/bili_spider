import csv

ls_in = ['csv文件', '含英文(,)的特殊情况']

with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(ls_in)

with open('data.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    ls_out = list(reader)[0]

print('ls_in:', ls_in, '\n长度=', len(ls_in))
print('ls_out:', ls_in, '\n长度=', len(ls_out))
