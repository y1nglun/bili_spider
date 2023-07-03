import scrapy
from scrapy import Request
import re
from douban_spider.items import DoubanSpiderItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    TOTAL_PAGE = 10

    cookies = {
        'll': '"108288"',
        'bid': 'Z_3vBiV0kFs',
        '__yadk_uid': 'TMVLAENOBkftolAgRlNPIueGpWua0kX4',
        '_vwo_uuid_v2': 'D28773AA2EE3F0E2F20E0ADE9004D9CD8|e568fb4ed1c269638799a6da4691ed0c',
        'douban-fav-remind': '1',
        'dbcl2': '"186160890:EjnkiO9pknM"',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        'ct': 'y',
        '__utmv': '30149280.18616',
        '__utmz': '223695111.1686790283.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '_pk_id.100001.4cf6': '24aa590f75720e57.1681197762.',
        '_ga': 'GA1.1.1241984296.1685431973',
        '_ga_RXNMP372GL': 'GS1.1.1686841532.1.1.1686842015.60.0.0',
        '__utmz': '30149280.1686977253.6.5.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/book/subject_search',
        'ck': 'i5eL',
        '__utmc': '30149280',
        '__utmc': '223695111',
        'ap_v': '0,6.0',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1687163986%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D',
        '_pk_ses.100001.4cf6': '1',
        'frodotk_db': '"799f03b40fbb8dbb6cdd0b1c2f32a931"',
        '__utma': '30149280.1241984296.1685431973.1687155070.1687164724.8',
        '__utma': '223695111.2136563401.1685431973.1687155070.1687164724.4',
        '__utmb': '223695111.0.10.1687164724',
        '__utmt': '1',
        '__utmb': '30149280.10.10.1687164724',
    }

    def start_requests(self):
        for page in range(0, self.TOTAL_PAGE * 25, 25):
            url = f'https://movie.douban.com/top250?start={page}&filter='
            print('scraping:', url)
            yield Request(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        items = response.css('.item')
        for item in items:
            name = item.css('.title::text').extract_first()
            href = item.css('.hd a::attr(href)').extract_first()
            image = item.css('.pic img::attr(src)').extract_first()
            score = item.css('.rating_num::text').extract_first()

            movie_item = DoubanSpiderItem()
            movie_item['name'] = name
            movie_item['href'] = href
            movie_item['image'] = image
            movie_item['score'] = score

            print('scraping detail:', href)

            yield Request(href, callback=self.parse_detail, cookies=self.cookies,
                          meta={'movie_item': movie_item})

    def parse_detail(self, response):
        movie_item = response.meta['movie_item']

        all_des = response.css('.indent .all::text').extract_first()
        info_text = response.css('#info').getall()
        country_match = re.search(r'制片国家/地区:</span> (.+)<br>', ''.join(info_text))
        if country_match:
            country = country_match.group(1).strip()
        else:
            country = None
        comment_href = response.css('#comments-section .mod-hd h2 .pl a::attr(href)').get()
        movie_item['all_des'] = all_des
        movie_item['country'] = country

        print('scraping comment:', comment_href)
        yield Request(comment_href, callback=self.parse_comment, meta={'movie_item': movie_item})

    def parse_comment(self, response):
        movie_item = response.meta['movie_item']

        for item in response.css('.comment-item'):
            user_name = item.css('.comment-info a::text').extract_first()
            comment_time = item.css('.comment-time::text').extract_first().strip()
            comment = item.css('.short::text').extract_first()

            movie_item['user_name'] = user_name
            movie_item['comment_time'] = comment_time
            movie_item['comment'] = comment

            yield movie_item
