# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TxComicSpiderItem(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    desc = scrapy.Field()
