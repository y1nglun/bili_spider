# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JzscSpiderItem(scrapy.Item):
    fr_name = scrapy.Field()
    qy_name = scrapy.Field()
    qy_code = scrapy.Field()
    qy_region_name = scrapy.Field()
