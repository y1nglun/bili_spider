import json

import scrapy
from scrapy.http import Request, FormRequest
from JYKS.items import JyksItem


class JykspqSpider(scrapy.Spider):
    name = "JYKSPQ"
    allowed_domains = ["read.douban.com"]
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'll="108288"; bid=Z_3vBiV0kFs; douban-fav-remind=1; dbcl2="186160890:EjnkiO9pknM"; push_noty_num=0; push_doumail_num=0; ct=y; __utmv=30149280.18616; __utma=30149280.1241984296.1685431973.1686728135.1686790232.5; __utmz=30149280.1686790232.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck=i5eL; _pk_id.100001.a7dd=2f8379ffc0246f5f.1686836543.1.1686836552.1686836543.',
        'Origin': 'https://read.douban.com',
        'Referer': 'https://read.douban.com/category/111?sort=hot&page=2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-CSRF-Token': 'i5eL',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    cookies = {
        'll': '"108288"',
        'bid': 'Z_3vBiV0kFs',
        'douban-fav-remind': '1',
        'dbcl2': '"186160890:EjnkiO9pknM"',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        'ct': 'y',
        '__utmv': '30149280.18616',
        '__utma': '30149280.1241984296.1685431973.1686728135.1686790232.5',
        '__utmz': '30149280.1686790232.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'ck': 'i5eL',
        '_pk_id.100001.a7dd': '2f8379ffc0246f5f.1686836543.1.1686836552.1686836543.',
    }

    def start_requests(self):
        for page in range(1, 10):
            url = 'https://read.douban.com/j/kind/'
            json_data = {
                'sort': 'hot',
                'page': page,
                'kind': 111,
                'query': '\n    query getFilterWorksList($works_ids: [ID!]) {\n      worksList(worksIds: $works_ids) {\n        \n    \n    title\n    cover(useSmall: false)\n    url\n    isBundle\n    coverLabel(preferVip: true)\n  \n    \n  url\n  title\n\n    \n  author {\n    name\n    url\n  }\n  origAuthor {\n    name\n    url\n  }\n  translator {\n    name\n    url\n  }\n\n    \n  abstract\n  authorHighlight\n  editorHighlight\n\n    \n    isOrigin\n    kinds {\n      \n    name @skip(if: true)\n    shortName @include(if: true)\n    id\n  \n    }\n    ... on WorksBase @include(if: true) {\n      wordCount\n      wordCountUnit\n    }\n    ... on WorksBase @include(if: false) {\n      inLibraryCount\n    }\n    ... on WorksBase @include(if: false) {\n      \n    isEssay\n    \n    ... on EssayWorks {\n      favorCount\n    }\n  \n    \n    \n    averageRating\n    ratingCount\n    url\n    isColumn\n    isFinished\n  \n  \n  \n    }\n    ... on EbookWorks @include(if: false) {\n      \n    ... on EbookWorks {\n      book {\n        url\n        averageRating\n        ratingCount\n      }\n    }\n  \n    }\n    ... on WorksBase @include(if: false) {\n      isColumn\n      isEssay\n      onSaleTime\n      ... on ColumnWorks {\n        updateTime\n      }\n    }\n    ... on WorksBase @include(if: true) {\n      isColumn\n      ... on ColumnWorks {\n        isFinished\n      }\n    }\n    ... on EssayWorks {\n      essayActivityData {\n        \n    title\n    uri\n    tag {\n      name\n      color\n      background\n      icon2x\n      icon3x\n      iconSize {\n        height\n      }\n      iconPosition {\n        x y\n      }\n    }\n  \n      }\n    }\n    highlightTags {\n      name\n    }\n    ... on WorksBase @include(if: false) {\n      fanfiction {\n        tags {\n          id\n          name\n          url\n        }\n      }\n    }\n  \n    \n  ... on WorksBase {\n    copyrightInfo {\n      newlyAdapted\n      newlyPublished\n      adaptedName\n      publishedName\n    }\n  }\n\n    isInLibrary\n    ... on WorksBase @include(if: false) {\n      \n    fixedPrice\n    salesPrice\n    isRebate\n  \n    }\n    ... on EbookWorks {\n      \n    fixedPrice\n    salesPrice\n    isRebate\n  \n    }\n    ... on WorksBase @include(if: true) {\n      ... on EbookWorks {\n        id\n        isPurchased\n        isInWishlist\n      }\n    }\n    ... on WorksBase @include(if: false) {\n      fanfiction {\n        fandoms {\n          title\n          url\n        }\n      }\n    }\n    ... on WorksBase @include(if: false) {\n      fanfiction {\n        kudoCount\n      }\n    }\n  \n        id\n        isOrigin\n        isEssay\n      }\n    }\n  ',
                'variables': {},
            }
            yield FormRequest(url, headers=self.headers, body=json.dumps(json_data), cookies=self.cookies,
                              callback=self.parse)

    def parse(self, response):
        for item in response.json()['list']:
            title = item['title']
            if item['author']:
                author = item['author'][0]['name'].strip()
            else:
                author = item['origAuthor'][0]['name'].strip()
            price = item['salesPrice']
            formatted_price = f"{int(price) / 100:.2f}"
            wordCount = item['wordCount']

            print(title, price, author, wordCount)

            book_item = JyksItem()
            book_item['name'] = title
            book_item['author'] = author
            book_item['price'] = formatted_price
            book_item['wordCount'] = wordCount

            yield book_item
