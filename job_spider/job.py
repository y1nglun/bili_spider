import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}
with open('output.txt', 'w', encoding='utf-8') as file:
    for page in range(1, 5):
        url = 'https://www.job001.cn/jobs?pageNo={}'.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all(attrs={'class': 'jobs_Con'})
        for item in items:
            job_name = item.find(attrs={'class': 'jobNameCon'}).get_text().strip()
            name = item.find(attrs={'class': 'jobRight'}).dl.dt.get_text().strip()
            salary = item.find(attrs={'class': 'salaryList'}).get_text().strip()
            city = item.find(attrs={'class': 'cityConJobsWork'}).get_text().strip()
            time = item.find(attrs={'class': 'time'}).get_text().strip()
            line = '|'.join([job_name, name, salary, city, time]) + '\n'
            file.write(line)
            print(job_name, name, salary, city, time)
