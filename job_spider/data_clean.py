import csv
import re

with open('job_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data_list = list(reader)

cleaned_data = []
for row in data_list:
    cleaned_row = []
    for field in row:
        cleaned_field = re.sub(r'\(面议\)', '', field)  # 删除"(面议)"
        cleaned_field = re.sub(r'\s+', ' ', cleaned_field).strip().replace('\n', '').replace('\r', '')  # 去除空格和换行符
        cleaned_row.append(cleaned_field)
    cleaned_data.append(cleaned_row)

with open('cleaned_job_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(cleaned_data)

print("数据清理完成！")
