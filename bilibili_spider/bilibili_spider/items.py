# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliSpiderItem(scrapy.Item):
    author = scrapy.Field()
    bvid = scrapy.Field()
    tag = scrapy.Field()
    title = scrapy.Field()
    typeid = scrapy.Field()
    arcurl = scrapy.Field()
    aid = scrapy.Field()
    play = scrapy.Field()
    danmaku = scrapy.Field()
    duration = scrapy.Field()
