import scrapy
from scrapy import Request
from scrapy.selector import Selector
from tianqiw_spider.items import TianqiwSpiderItem


class TianqiwSpider(scrapy.Spider):
    name = "tianqiw"
    allowed_domains = ["tianqi.com"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for mon in range(1, 7):
            month_str = str(mon).zfill(2)  # 将月份转换为两位数的字符串
            url = f'https://lishi.tianqi.com/beijing/2023{month_str}.html'
            yield Request(url, headers=self.headers, meta={'month': mon}, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        # 使用CSS选择器提取数据
        high = sel.css('.tian_two li')[0].css('.tian_twoa::text').get()  # 最高温度
        low = sel.css('.tian_two li')[0].css('.tian_twoa::text')[1].get()  # 最低温度
        air_best = sel.css('.tian_two li')[4].css('.tian_twoa::text')[0].get()  # 空气质量最好指数
        air_low = sel.css('.tian_two li')[5].css('.tian_twoa::text')[0].get()  # 空气质量最差指数
        month = response.meta['month']  # 从请求的元数据中获取月份
        print(low, high, air_low, air_best)

        item = TianqiwSpiderItem()
        item['high'] = high
        item['low'] = low
        item['air_best'] = air_best
        item['air_low'] = air_low
        item['month'] = month

        yield item
