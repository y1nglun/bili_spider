import requests
from bs4 import BeautifulSoup
import pymongo

TOTAL_PAGE = 10

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['douban']
collection = db['top250']


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('.item')
    for item in items:
        name = item.select_one('.title').text
        href = item.select_one('.hd a')['href']
        image = item.select_one('.pic img')['src']
        score = item.select_one('.rating_num').text
        print('name:{}----*-----rate:{}-----*------image:{}----*-----href:{}'.format(name, score, image, href))
        collection.update_one({'name': name}, {'$set': {'name': name,
                                                        'image': image,
                                                        'score': score,
                                                        'link': href
                                                        }}, True)


if __name__ == '__main__':
    for page in range(0, TOTAL_PAGE * 25, 25):
        response = requests.get('https://movie.douban.com/top250?start={}&filter='.format(page), headers=headers)
        print(response.url)
        parse_page(response.text)
