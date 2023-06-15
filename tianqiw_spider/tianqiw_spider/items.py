# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianqiwSpiderItem(scrapy.Item):
    high = scrapy.Field()
    low = scrapy.Field()
    air_best = scrapy.Field()
    air_low = scrapy.Field()
    month = scrapy.Field()
