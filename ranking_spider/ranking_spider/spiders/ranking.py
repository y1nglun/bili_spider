import scrapy
from scrapy import Request
import re
import execjs
from ranking_spider.items import RankingSpiderItem


class RankingSpider(scrapy.Spider):
    name = "ranking"
    allowed_domains = ["shanghairanking.cn"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 Safari/537.36"
    }

    start_url = 'https://shanghairanking.cn/_nuxt/static/1686903314/rankings/bcur/202211/payload.js'

    def start_requests(self):
        # 发起初始请求，指定回调函数为parse
        yield Request(self.start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # 从响应中提取匹配的内容
        pattern = r'__NUXT_JSONP__\("/rankings/bcur/202211", \((.*?)\)\);'
        result = re.search(pattern, response.text)
        if result:
            matched_content = result.group(1)
        else:
            print("No match found.")

        # 使用execjs执行JavaScript代码
        ctx = execjs.compile('')  # 在这里填入相应的JavaScript代码
        result = ctx.eval(matched_content)
        for items in result['data']:
            for school in items['univData']:
                # 解析每个学校的数据
                univNameCn = school['univNameCn']
                univNameEn = school['univNameEn']
                score = school['score']
                univCategory = school['univCategory']
                ranking = school['ranking']
                province = school['province']
                univTags = school['univTags']

                # 打印学校的信息
                print('ranking:', ranking)
                print("univNameCn:", univNameCn)
                print('univTags:', univTags)
                print('province:', province)

                # 创建RankingSpiderItem对象并返回
                item = RankingSpiderItem()
                item['ranking'] = ranking
                item['univNameCn'] = univNameCn
                item['univNameEn'] = univNameEn
                item['score'] = score
                item['univCategory'] = univCategory
                item['univTags'] = univTags
                yield item
