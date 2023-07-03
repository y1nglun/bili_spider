import tkinter as tk
from tkinter import messagebox
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from wordcloud import WordCloud
from PIL import ImageTk
import ast

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
params = {
    'keyType': '0',
    'keyWord': '长沙',
    'jobTypeId': '',
    'jobType': '职位类型',
    'industry': '',
    'industryname': '行业类型',
    'workId': '',
    'workPlace': '',
    'salary': '',
    'salaryType': '',
    'entType': '',
    'experience': '',
    'education': '',
    'entSize': '',
    'benefits': '',
    'reftime': '',
    'workTypeId': '',
    'sortField': '',
    'pageNo': '1',
    'curItem': '',
    'searchType': '1',
}


def extract_job_data(url):
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all(attrs={'class': 'jobs_Con'})

    for item in items:
        job_name = item.find(attrs={'class': 'jobNameCon'}).get_text().strip()
        name = item.find(attrs={'class': 'jobRight'}).dl.dt.get_text().strip()
        salary_raw = item.find(attrs={'class': 'salaryList'}).get_text().strip()
        salary = salary_raw.replace("\n", "").strip()
        city = item.find(attrs={'class': 'cityConJobsWork'}).get_text().strip()
        time = item.find(attrs={'class': 'time'}).get_text().strip()
        link = item.select_one('.mouseListenTop a')['href']

        print(job_name, name, salary, city, time)
        detail_list, content = extract_job_detail(link)

        data = [job_name, name, salary, city, time, detail_list, content]
        save_to_csv(data, 'job_data.csv')


def extract_job_detail(link):
    detail_list = []
    base_url = 'https://www.job001.cn/'
    detail_url = urljoin(base_url, link)
    response = requests.get(detail_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    detail_info_list = soup.select('.detail_info ul li')
    for i in detail_info_list:
        detail_list.append(i.get_text())
    job_content = soup.select_one('.jobs_content_other')
    if job_content:
        content = job_content.get_text()
    else:
        content = ''
    return detail_list, content


def save_to_csv(data, file_path):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def crawl_jobs():
    # 设置CSV文件的表头
    header = ['职位名称', '公司名称', '薪资', '城市', '发布时间', '详细信息', '内容']
    # 写入表头
    save_to_csv(header, 'job_data.csv')

    for page in range(1, 10):
        url = 'https://www.job001.cn/jobs?pageNo={}'.format(page)
        extract_job_data(url)

    messagebox.showinfo('提示', '数据保存成功！')


def read_data():
    with open('cleaned_job_data.csv', mode='r', encoding='utf-8') as file:
        data = file.readlines()

        text_box.delete('1.0', tk.END)

        for i, line in enumerate(data, start=1):
            text = f'({i}). {line}'
            text_box.insert(tk.END, text)


def clean_data():
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

    messagebox.showinfo('提示', '数据清理完成！')


def show_personal_info():
    personal_info = {
        '姓名': 'Your Name',
        '学号': 'Your Student ID',
        '班级': 'Your Class'
    }
    info_str = '\n'.join([f'{key}: {value}' for key, value in personal_info.items()])
    messagebox.showinfo('个人信息', info_str)


def generate_wordcloud():
    # 读取CSV文件
    with open('cleaned_job_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        detailed_info = [ast.literal_eval(row['详细信息']) for row in reader]

    text_list = list(set([item for sublist in detailed_info for item in sublist]))

    text = ' '.join(text_list)

    wordcloud = WordCloud(background_color='white', font_path='C:/Windows/Fonts/msyh.ttc').generate(text)

    image = wordcloud.to_image()

    image_tk = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=image_tk)
    label.image = image_tk
    label.pack()


# 创建主窗口
window = tk.Tk()
window.geometry('800x600')
window.title('前程无忧爬虫及可视化展示')

title_label = tk.Label(window, text='前程无忧爬虫及可视化展示', font=('Arial', 16, 'bold'))
title_label.pack(pady=10)

button_frame = tk.Frame(window)
button_frame.pack()

personal_info_button = tk.Button(button_frame, text='个人信息', command=show_personal_info)
personal_info_button.pack(side='left', padx=10)

crawl_button = tk.Button(button_frame, text='开始爬取', command=crawl_jobs)
crawl_button.pack(side='left', padx=10)

clean_button = tk.Button(button_frame, text='数据清理', command=clean_data)
clean_button.pack(side='left', padx=10)

read_button = tk.Button(button_frame, text='读取数据', command=read_data)
read_button.pack(side='left', padx=10)

wordcloud_button = tk.Button(button_frame, text='生成词云图', command=generate_wordcloud)
wordcloud_button.pack(side='left', padx=10)

text_box = tk.Text(window, height=20, width=80)
text_box.pack(pady=10)

window.mainloop()
