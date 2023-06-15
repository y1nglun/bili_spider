import scrapy
from scrapy import Request, FormRequest
import execjs
from qimingpian_spider.items import QimingpianSpiderItem


class QimingpianSpider(scrapy.Spider):
    name = "qimingpian"
    allowed_domains = ["qimingpian.com"]
    start_url = 'https://vipapi.qimingpian.cn/DataList/productListVip'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        for page in range(1, 3):
            formdata = {
                'time_interval': '',
                'tag': '',
                'tag_type': 'and',
                'province': '',
                'lunci': '',
                'page': f'{page}',
                'num': '20',
                'unionid': 'i / Xkq5C5BNcokHyyn8JQwK7SpcFrSbF2Aptks9UCuAIuErPuHZY30t8LaGL2Czn0eJWqqIs6kiQsM8IbOYgM5A ==',
            }
            yield FormRequest(self.start_url, formdata=formdata, headers=self.headers, callback=self.parse_start)

    def parse_start(self, response):
        res = response.json()
        encrypt_data = res['encrypt_data']
        with open('E:\spider\spider\qimingpian_spider\qimingpian_spider\js\qimingpian.js', 'r', encoding='utf-8') as f:
            jscode = f.read()

        ctx = execjs.compile(jscode).call('s', encrypt_data)
        for item in ctx['list']:
            product = item['product']
            icon_url = item['icon']
            hangye1 = item['hangye1']
            yewu = item['yewu']
            province = item['province']
            money = item['money']
            time = item['time']

            product_item = QimingpianSpiderItem()
            product_item['product'] = product
            product_item['icon_url'] = icon_url
            product_item['hangye1'] = hangye1
            product_item['yewu'] = yewu
            product_item['province'] = province
            product_item['money'] = money
            product_item['time'] = time
            yield item
