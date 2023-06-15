import time

import scrapy
from scrapy import Request
from urllib.parse import urlencode
from bilibili_spider.items import BilibiliSpiderItem


class BiliSpider(scrapy.Spider):
    name = "bili"
    allowed_domains = ["bilibili.com"]

    cookies = {
        'buvid3': 'C4C1727A-5E91-1950-9991-BF23CE9AC47489923infoc',
        'b_nut': '1680164789',
        '_uuid': '65B83A75-F4DE-A26B-4E61-3FFF10DF7218690586infoc',
        'is-2022-channel': '1',
        'nostalgia_conf': '-1',
        'CURRENT_FNVAL': '4048',
        'CURRENT_PID': 'b4e1d100-ced4-11ed-a310-2b7f43704e84',
        'rpdid': "|(J~kkk|m|||0J'uY)|uYR)R~",
        'i-wanna-go-back': '-1',
        'header_theme_version': 'CLOSE',
        'CURRENT_QUALITY': '80',
        'b_ut': '5',
        'buvid4': 'DC5F1645-DCF9-048B-919E-E88583CE1A6190797-023033016-9k5epjPVrQuPAeu4%2Fh%2FqLA%3D%3D',
        'FEED_LIVE_VERSION': 'V8',
        'fingerprint': '3b9ec79f5d87be547d9ca47c22c21e66',
        'buvid_fp_plain': 'undefined',
        'DedeUserID': '108867418',
        'DedeUserID__ckMd5': 'ae016d32e1151f79',
        'buvid_fp': '3b9ec79f5d87be547d9ca47c22c21e66',
        'bp_video_offset_108867418': '803606016478412800',
        'home_feed_column': '4',
        'hit-new-style-dyn': '0',
        'hit-dyn-v2': '1',
        'SESSDATA': '3448427a%2C1702040261%2Cb65cc%2A61',
        'bili_jct': '24f3aa23109ba9fd5032ebe595489233',
        'sid': '82d2uo7u',
        'browser_resolution': '1280-657',
        'innersign': '0',
        'b_lsid': 'CD2D2DAA_188B26D5497',
        'PVID': '1',
    }

    headers = {
        'authority': 'api.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'cookie': "buvid3=C4C1727A-5E91-1950-9991-BF23CE9AC47489923infoc; b_nut=1680164789; _uuid=65B83A75-F4DE-A26B-4E61-3FFF10DF7218690586infoc; is-2022-channel=1; nostalgia_conf=-1; CURRENT_FNVAL=4048; CURRENT_PID=b4e1d100-ced4-11ed-a310-2b7f43704e84; rpdid=|(J~kkk|m|||0J'uY)|uYR)R~; i-wanna-go-back=-1; header_theme_version=CLOSE; CURRENT_QUALITY=80; b_ut=5; buvid4=DC5F1645-DCF9-048B-919E-E88583CE1A6190797-023033016-9k5epjPVrQuPAeu4%2Fh%2FqLA%3D%3D; FEED_LIVE_VERSION=V8; fingerprint=3b9ec79f5d87be547d9ca47c22c21e66; buvid_fp_plain=undefined; DedeUserID=108867418; DedeUserID__ckMd5=ae016d32e1151f79; buvid_fp=3b9ec79f5d87be547d9ca47c22c21e66; bp_video_offset_108867418=803606016478412800; home_feed_column=4; hit-new-style-dyn=0; hit-dyn-v2=1; SESSDATA=3448427a%2C1702040261%2Cb65cc%2A61; bili_jct=24f3aa23109ba9fd5032ebe595489233; sid=82d2uo7u; browser_resolution=1280-657; innersign=0; b_lsid=CD2D2DAA_188B26D5497; PVID=1",
        'origin': 'https://search.bilibili.com',
        'referer': 'https://search.bilibili.com/all?vt=20693543&keyword=jk&from_source=webtop_search&spm_id_from=333.1007&search_source=3&page=5&o=120',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'

    def start_requests(self):
        for page in range(1, 35):
            t = time.time()
            params = {
                '__refresh__': 'true',
                '_extra': '',
                'context': '',
                'page': f'{page}',
                'page_size': '42',
                'from_source': '',
                'from_spmid': '333.337',
                'platform': 'pc',
                'highlight': '1',
                'single_column': '0',
                'keyword': 'jk',
                'qv_id': 'vHhgy4OzCqYQaQWNXLGbjhYIQfQhNI0I',
                'ad_resource': '5654',
                'source_tag': '3',
                'gaia_vtoken': '',
                'category_id': '',
                'search_type': 'video',
                'dynamic_offset': '120',
                'web_location': '1430654',
                'w_rid': '3a46e78fabff8a51e68adda419f86bc7',
                'wts': f'{t}',
            }
            encoded_params = urlencode(params)
            yield Request(url='?'.join([self.url, encoded_params]), headers=self.headers, cookies=self.cookies,
                          callback=self.parse)

    def parse(self, response):
        js = response.json()
        for data in js['data']['result']:
            author = data['author']
            bvid = data['bvid']
            tag = data['tag']
            title = data['title']
            typeid = data['typeid']
            arcurl = data['arcurl']
            aid = data['aid']
            danmaku = data['danmaku']
            play = data['play']
            duration = data['duration']

            item = BilibiliSpiderItem()
            item['author'] = author
            item['bvid'] = bvid
            item['tag'] = tag
            item['title'] = title
            item['typeid'] = typeid
            item['arcurl'] = arcurl
            item['aid'] = aid
            item['danmaku'] = danmaku
            item['play'] = play
            item['duration'] = duration

            yield item
