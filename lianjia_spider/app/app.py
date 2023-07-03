import requests
import csv
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import ImageTk, Image

font_path = 'C:/Windows/Fonts/STHUPO.TTF'
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

data = []
image_visible = True


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    data = []
    for item in soup.select('.sellListContent li'):
        title_elem = item.select_one('.title a')
        detail_elem = item.select_one('.houseInfo')
        total_price_elem = item.select_one('.totalPrice span')
        price_elem = item.select_one('.unitPrice span')

        if title_elem and detail_elem and total_price_elem and price_elem:
            title = title_elem.get_text()
            detail = detail_elem.get_text()
            total_price = total_price_elem.get_text()
            price = price_elem.get_text()

            data.append({
                '标题': title,
                '房屋详细信息': detail,
                '总价': total_price,
                '单价': price
            })

    return data


def crawl_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    total_data = []

    for page in range(1, 11):
        url = f'https://zz.lianjia.com/ershoufang/pg{page}/'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_data = parse(response.text)
            total_data.extend(page_data)
        else:
            messagebox.showerror('错误', f'第 {page} 页爬取失败！')

    global data
    data = total_data
    save_to_excel(data)
    show_data(data)
    messagebox.showinfo('提示', '爬虫数据获取成功！')


def save_to_excel(data):
    file_path = 'lianjia_data.xlsx'
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)


def read_from_excel():
    file_path = 'lianjia_data.xlsx'
    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except FileNotFoundError:
        return []


def show_data(data):
    # 清空显示区域
    text.delete('1.0', tk.END)

    for item in data:
        text.insert(tk.END, f"标题：{item['标题']}\n")
        text.insert(tk.END, f"房屋详细信息：{item['房屋详细信息']}\n")
        text.insert(tk.END, f"总价：{item['总价']}\n")
        text.insert(tk.END, f"单价：{item['单价']}\n")
        text.insert(tk.END, "===============================\n")


def search_data():
    keyword = entry.get()

    if keyword:
        filtered_data = [item for item in data if keyword in item['标题']]
        show_data(filtered_data)
    else:
        show_data(data)


def visualize_price_distribution():
    df = pd.read_excel('lianjia_data.xlsx')
    plt.figure(figsize=(10, 6))
    plt.hist(df['总价'], bins=10, edgecolor='black')
    plt.xlabel('房屋总价')
    plt.ylabel('数量')
    plt.title('房屋总价分布')
    plt.grid(True)
    plt.savefig('price_distribution.png')
    plt.close()
    display_image('price_distribution.png')


def visualize_price_relation():
    df = pd.read_excel('lianjia_data.xlsx')
    plt.figure(figsize=(10, 6))
    prices = df['单价'].str.replace(',', '').str.extract(r'(\d+)').astype(int)
    plt.scatter(prices, df['总价'], alpha=0.5)
    plt.xlabel('单价')
    plt.ylabel('总价')
    plt.title('单价与总价关系')
    plt.grid(True)
    plt.savefig('price_relation.png')
    plt.close()
    display_image('price_relation.png')


def display_image(image_path):
    image = Image.open(image_path)
    image = image.resize((400, 300), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo


window = tk.Tk()
window.title("链家爬虫")
window.geometry("800x600")

frame_top = tk.Frame(window)
frame_top.pack(pady=10)

button_crawl = tk.Button(frame_top, text="开始爬虫", command=crawl_data)
button_crawl.pack(side=tk.LEFT, padx=5)

button_visualize_price_distribution = tk.Button(frame_top, text="房屋总价分布", command=visualize_price_distribution)
button_visualize_price_distribution.pack(side=tk.LEFT, padx=5)

button_visualize_price_relation = tk.Button(frame_top, text="单价与总价关系", command=visualize_price_relation)
button_visualize_price_relation.pack(side=tk.LEFT, padx=5)

frame_search = tk.Frame(window)
frame_search.pack(pady=10)

label_search = tk.Label(frame_search, text="关键字搜索：")
label_search.pack(side=tk.LEFT)

entry = tk.Entry(frame_search)
entry.pack(side=tk.LEFT, padx=5)

button_search = tk.Button(frame_search, text="搜索", command=search_data)
button_search.pack(side=tk.LEFT, padx=5)

text = tk.Text(window)
text.pack(fill=tk.BOTH, expand=True)

image_label = tk.Label(window)
image_label.pack(side=tk.TOP, padx=10, pady=10)

data = read_from_excel()

show_data(data)

window.mainloop()
