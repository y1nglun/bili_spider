import random
import time

import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.font_manager as fm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/111.0.0.0 Safari/537.36"
}

movies = []  # 声明为全局变量

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

window = None
canvas = None
figure = None


def visualizeYearCounts():
    global window, canvas, figure
    # 读取Excel表格数据
    df = pd.read_excel('movies.xlsx')

    # 统计年份分布
    year_counts = df['年份'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(year_counts.index, year_counts.values)
    ax.set_xlabel('年份')
    ax.set_ylabel('电影数量')
    ax.set_title('电影年份分布')

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    if figure is not None:
        plt.close(figure)

    # 创建画布并将图表显示在画布上
    figure = fig
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def visualizeGenreCounts():
    global window, canvas, figure
    # 读取Excel表格数据
    df = pd.read_excel('movies.xlsx')

    # 统计年份分布

    # 统计类型分布
    genre_counts = df['类型'].value_counts()

    # 创建图表
    fig, ax = plt.subplots()
    ax.pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('电影类型分布')

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    if figure is not None:
        plt.close(figure)

    # 创建画布并将图表显示在画布上
    figure = fig
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


# 创建评分分布柱状图
def visualizeRatingCounts():
    global window, canvas, figure
    df = pd.read_excel('movies.xlsx')
    # 统计评分分布
    rating_counts = df['评分'].value_counts().sort_index()

    # 创建图表
    fig, ax = plt.subplots()
    ax.bar(rating_counts.index, rating_counts.values)
    ax.set_xlabel('评分')
    ax.set_ylabel('电影数量')
    ax.set_title('电影评分分布')

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    if figure is not None:
        plt.close(figure)

    # 创建画布并将图表显示在画布上
    figure = fig
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def getHTMLText(url):
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except:
        return ''


def parseHTML(html):
    movies = []  # 在函数内部声明movies列表
    soup = BeautifulSoup(html, 'lxml')
    for item in soup.select('.doulist-subject'):
        title = item.select_one('.title a').get_text().strip()
        rating = item.select_one('.rating_nums').get_text().strip()
        comment_match = re.search(r'\((.*?)评价\)', item.select_one('.rating').get_text().strip())
        if comment_match:
            comment = comment_match.group(1)
        else:
            comment = ''
        abstract = item.select_one('.abstract').get_text().strip()
        director_pattern = r'导演:\s*(.*)'
        actor_pattern = r'主演:\s*(.*)'
        genre_pattern = r'类型:\s*(.*)'
        year_pattern = r'年份:\s*(\d+)'

        director_match = re.search(director_pattern, abstract)
        actor_match = re.search(actor_pattern, abstract)
        genre_match = re.search(genre_pattern, abstract)
        year_match = re.search(year_pattern, abstract)

        director = director_match.group(1) if director_match else None
        actor = actor_match.group(1) if actor_match else None
        genre = genre_match.group(1) if genre_match else None
        year = year_match.group(1) if year_match else None

        movies.append([title, rating, comment, director, actor, genre, year])

    return movies


def saveToExcel(movies):
    df = pd.DataFrame(movies, columns=['电影名称', '评分', '评价人数', '导演', '主演', '类型', '年份'])
    df.to_excel('movies.xlsx', index=False)
    messagebox.showinfo('保存成功', '电影数据保存成功！')


def scrapeMovies():
    global movies  # 使用全局变量movies
    movies = []  # 清空movies列表
    for offset in range(0, 50, 25):
        url = f'https://www.douban.com/doulist/137843346/?start={offset}&sort=seq&playable=0&sub_type='
        html = getHTMLText(url)
        movies += parseHTML(html)
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)
    saveToExcel(movies)


def main():
    global window, canvas, figure  # 声明全局变量

    # 创建窗体
    window = tk.Tk()
    window.title("电影爬虫与可视化")

    # 创建标签
    label = tk.Label(window, text="点击按钮开始爬取电影信息并进行可视化", font=("Arial", 14))
    label.pack(pady=10)

    # 创建按钮
    button1 = tk.Button(window, text="爬取电影信息", command=scrapeMovies)
    button1.pack(pady=5)

    button2 = tk.Button(window, text="可视化电影年份分布", command=visualizeYearCounts)
    button2.pack(pady=5)

    # 创建按钮3，用于显示评分分布柱状图
    button3 = tk.Button(window, text="显示评分分布", command=visualizeRatingCounts)
    button3.pack(pady=5)

    button4 = tk.Button(window, text="显示类型分布", command=visualizeGenreCounts)
    button4.pack(pady=5)

    # 创建空白画布
    figure = plt.Figure(figsize=(6, 5), dpi=100)
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # 运行窗体主循环
    window.mainloop()


if __name__ == "__main__":
    main()
