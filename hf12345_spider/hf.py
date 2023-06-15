import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

base_url = 'http://www.hf12345.org/'


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def scrape_page(session, page):
    url = f'http://www.hf12345.org/ywbb/?page={page}'
    print('scraping url:', url)
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'lxml')

    rows = []
    for item in soup.select('.indexnews tr'):
        content = item.text.strip().split('\n')
        date = content[1]
        link = item.select_one('a')['href']
        detail_url = urljoin(base_url, link)
        print('scraping detail:', detail_url)

        html = await fetch(session, detail_url)
        soup = BeautifulSoup(html, 'lxml')
        title_match = soup.select_one('.news_nei_title_h1')
        if title_match:
            title = title_match.get_text().strip()
        else:
            title = ''
        detail_match = soup.select_one('.newscontent')
        if detail_match:
            detail = detail_match.get_text().strip().replace('\n', '')
        else:
            detail = ''

        rows.append([title, date, link, detail])

    return rows


async def scrape_pages():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, 49):
            task = asyncio.create_task(scrape_page(session, page))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # 将结果写入CSV文件
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Date', 'Link', 'Detail'])
            for rows in results:
                writer.writerows(rows)

    print('Scraping and writing to CSV completed.')


# 运行异步爬虫
asyncio.run(scrape_pages())
