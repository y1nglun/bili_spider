import math

import requests
from bs4 import BeautifulSoup

url = 'https://weibo.com/ajax/statuses/mymblog?'
start_url = 'https://weibo.com/ajax/statuses/mymblog?uid=2803301701&page=1&feature=0'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

cookie = 'WBPSESS=R5C0elPaDp4mis6NOqdmv_n8IIfDJO1XNV8tKKRXuy_mG7geWWHoSSPyXGBumGZVSlBaVogN6a971uGCPfQK6YugixhdLKgsP5Ih1nAd1tTVwxd_HP6KkcNR9UTjQDqI5zgX4SuCe1IyfFBL9iZ_mg==; XSRF-TOKEN=1vImCeSV267GofEPNkmO0LMR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhEcHdGNeNv0Oy9HFC-ldNs5JpX5KMhUgL.Fo-NSo2cShnceKe2dJLoIX5LxKqLBoeLBK2LxKnL122L1K.LxK-L1K2LBoeLxK-L1hBLB.qLxKML1-2L1hBLxK-L12qLB-qLxKBLBo.L1K5p; ALF=1688087949; SSOLoginState=1685495950; SCF=Av7DaJjQE-T3RioDuXNC1TCTLd4zbpQOMJ4KTOlyS8ZtBKV_l-tVEFWSh7GVm7MpXYLK98sGuNlc8y5Y1x8Rl6U.; SUB=_2A25JctDfDeRhGeNJ7VMX9CbKyj-IHXVqBkUXrDV8PUNbmtAGLVrckW9NRWMJepqH9eSRiZ7qsbrfVGij2s8BbLxw'


def scrape_start():
    print('scrape start')
    response = requests.get(start_url, headers=headers, cookies={'Cookie': cookie}).json()
    total_page, since_id = parse_index(response)
    scrape_late(total_page, since_id)


def scrape_late(total_page, since_id):
    for page in range(2, total_page + 1):
        print('current_page:', page)
        print(since_id)
        params = {
            "uid": "2803301701",
            "page": "{}".format(page),
            "feature": "0",
            "since_id": since_id
        }
        response = requests.get(url, cookies={'Cookie': cookie}, headers=headers, params=params).json()
        since_id = response['data']['since_id']
        parse_index(response)


def parse_index(response):
    total = response['data']['total']
    total_page = math.ceil(total / 20)
    since_id = response['data']['since_id']
    for data in response['data']['list']:
        pic_list = []
        soup = BeautifulSoup(data['text'], 'lxml')
        content = soup.get_text()
        create_at = data['created_at']
        attitudes_count = data['attitudes_count']
        reposts_count = data['reposts_count']
        comments_count = data['comments_count']
        if 'pic_ids' in data:
            pic_ids = data['pic_ids']
        if 'pic_infos' in data:
            for pic_id in pic_ids:
                pic_list.append(data['pic_infos'][pic_id]['thumbnail']['url'])
        print(
            'content:{}-----create_at:{}-----attitudes_count:{}-----resposts_count:{}-----comments_count:{}----pic_list:{}').format(
            content, create_at, attitudes_count, reposts_count, comments_count, pic_list)
    return total_page, since_id


if __name__ == '__main__':
    scrape_start()
