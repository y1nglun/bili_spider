import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}


def extract_job_data(url):
    response = requests.get(url, headers=headers)
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


header = ['职位名称', '公司名称', '薪资', '城市', '发布时间', '详细信息', '内容']

save_to_csv(header, 'job_data.csv')

for page in range(1, 10):
    url = 'https://www.job001.cn/jobs?pageNo={}'.format(page)
    extract_job_data(url)

print("数据保存成功！")
