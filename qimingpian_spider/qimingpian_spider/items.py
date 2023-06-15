# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QimingpianSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product = scrapy.Field()
    icon_url = scrapy.Field()
    hangye1 = scrapy.Field()
    yewu = scrapy.Field()
    province = scrapy.Field()
    money = scrapy.Field()
    time = scrapy.Field()
