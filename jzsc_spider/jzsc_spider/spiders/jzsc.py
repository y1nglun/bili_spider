import scrapy
from scrapy import Request, FormRequest
import execjs
from jzsc_spider.items import JzscSpiderItem


class JzscSpider(scrapy.Spider):
    name = "jzsc"
    allowed_domains = ["jzsc.mohurd.gov.cn"]
    start_url = 'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        for page in range(0, 30):
            yield Request(f'{self.start_url}?pg={page}&pgsz=15&total=450', headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = response.text
        with open('E:\spider\spider\jzsc_spider\jzsc_spider\js\jzsc.js') as f:
            jscode = f.read()

        ctx = execjs.compile(jscode).call('m', data)
        print(ctx)
        for item in ctx['data']['list']:
            fr_name = item['QY_FR_NAME']
            qy_name = item['QY_NAME']
            qy_code = item['QY_ORG_CODE']
            qy_region_name = item['QY_REGION_NAME']

            qy_item = JzscSpiderItem()
            qy_item['fr_name'] = fr_name
            qy_item['qy_name'] = qy_name
            qy_item['qy_code'] = qy_code
            qy_region_name['qy_region_name'] = qy_region_name
            yield qy_item
