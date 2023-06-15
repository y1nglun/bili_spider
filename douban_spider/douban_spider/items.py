# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSpiderItem(scrapy.Item):
    name = scrapy.Field()
    href = scrapy.Field()
    image = scrapy.Field()
    score = scrapy.Field()
