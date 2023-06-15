import scrapy
from scrapy import Request
from tx_comic_spider.items import TxComicSpiderItem


class TxComicSpider(scrapy.Spider):
    name = "tx_comic"
    allowed_domains = ["ac.qq.com"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        # 遍历页数
        for page in range(1, 100):
            url = f'https://ac.qq.com/Comic/all/page/{page}'
            print(f'正在爬取链接：{url}')
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # 解析每个漫画的信息
        for item in response.css('.ret-search-item'):
            tags = []
            title = item.css('.ret-works-title a::text').get()
            author = item.css('.ret-works-author::text').get()
            for tag in item.css('.ret-works-tags span::text'):
                tags.append(tag.get())
            desc = item.css('.ret-works-decs::text').get()

            # 打印提取的数据
            print(title, author, tags, desc)

            # 创建漫画数据项并传递数据
            comic = TxComicSpiderItem()
            comic['title'] = title
            comic['author'] = author
            comic['tags'] = tags
            comic['desc'] = desc

            # 返回数据项
            yield comic
