import scrapy
from scrapy import Request
from douban_spider.items import DoubanSpiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    TOTAL_PAGE = 10

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for page in range(0, self.TOTAL_PAGE * 25, 25):
            url = f'https://movie.douban.com/top250?start={page}&filter='
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        items = response.css('.item')
        for item in items:
            name = item.css('.title::text').extract_first()
            href = item.css('.hd a::attr(href)').extract_first()
            image = item.css('.pic img::attr(src)').extract_first()
            score = item.css('.rating_num::text').extract_first()
            print('name:{}----*-----rate:{}-----*------image:{}----*-----href:{}'.format(name, score, image, href))

            movie_item = DoubanSpiderItem()
            movie_item['name'] = name
            movie_item['href'] = href
            movie_item['image'] = image
            movie_item['score'] = score

            yield movie_item
