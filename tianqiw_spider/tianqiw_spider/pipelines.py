# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TianqiwSpiderPipeline:
    def process_item(self, item, spider):
        return item


class TxtPipeline(object):
    def open_spider(self, spider):
        self.file = open('weather.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write('month\tlow\thight\tair_low\tair_best\n')
        line = "{:<5}  {:<5}  {:<5}  {:<9}  {:<7}\n".format(
            item['month'], item['low'], item['high'], item['air_low'], item['air_best']
        )
        self.file.write(line)
        return item
