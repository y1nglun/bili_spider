# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RankingSpiderItem(scrapy.Item):
    ranking = scrapy.Field()
    univNameCn = scrapy.Field()
    univNameEn = scrapy.Field()
    score = scrapy.Field()
    univCategory = scrapy.Field()
    univTags = scrapy.Field()
    province = scrapy.Field()

