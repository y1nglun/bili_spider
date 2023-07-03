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
    all_des = scrapy.Field()
    country = scrapy.Field()
    user_name = scrapy.Field()
    comment_time = scrapy.Field()
    comment = scrapy.Field()
