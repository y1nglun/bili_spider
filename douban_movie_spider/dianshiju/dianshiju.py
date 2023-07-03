import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

movies = []

def getHTMLText(url):
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        return response.text
    except:
        return ''


def parseHTML(html):
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
    print("保存成功！")


def main():
    for offset in range(0, 50, 25):
        url = f'https://www.douban.com/doulist/137843346/?start={offset}&sort=seq&playable=0&sub_type='
        html = getHTMLText(url)
        movies = parseHTML(html)
    saveToExcel(movies)


main()
