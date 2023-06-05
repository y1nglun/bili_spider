import requests
from bs4 import BeautifulSoup
import pymongo
import json

cookies = {
    'Cookie': 'XSRF-TOKEN=1vImCeSV267GofEPNkmO0LMR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhEcHdGNeNv0Oy9HFC-ldNs5JpX5KMhUgL.Fo-NSo2cShnceKe2dJLoIX5LxKqLBoeLBK2LxKnL122L1K.LxK-L1K2LBoeLxK-L1hBLB.qLxKML1-2L1hBLxK-L12qLB-qLxKBLBo.L1K5p; ALF=1688087949; SSOLoginState=1685495950; SCF=Av7DaJjQE-T3RioDuXNC1TCTLd4zbpQOMJ4KTOlyS8ZtBKV_l-tVEFWSh7GVm7MpXYLK98sGuNlc8y5Y1x8Rl6U.; SUB=_2A25JctDfDeRhGeNJ7VMX9CbKyj-IHXVqBkUXrDV8PUNbmtAGLVrckW9NRWMJepqH9eSRiZ7qsbrfVGij2s8BbLxw; UPSTREAM-V-WEIBO-COM=35846f552801987f8c1e8f7cec0e2230; _s_tentry=weibo.com; Apache=9316508105185.26.1685525718491; SINAGLOBAL=9316508105185.26.1685525718491; ULV=1685525718551:1:1:1:9316508105185.26.1685525718491:; WBPSESS=R5C0elPaDp4mis6NOqdmv_n8IIfDJO1XNV8tKKRXuy_mG7geWWHoSSPyXGBumGZVK1v9r_djXtCdM9pWv5PvJTRMkI6juV27oG6bQz2htG8Rmng6sfVHtrmbwJsP34zk-tDxSi4fp_fAvkjPlceoFQ=='
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['weibo']
collection = db['comments']


def scrape_index(key_words):
    max_id = None
    for i in range(1000):
        params = {
            "list_id": "110005761648613",
            "refresh": "4",
            "since_id": "0",
            "count": "25",
            "fid": "110005761648613",
            "max_id": "{}".format(max_id)
        }
        try:
            response = requests.get('https://weibo.com/ajax/feed/friendstimeline', params=params, cookies=cookies,
                                    headers=headers).json()
            max_id = response['max_id_str']
            print(max_id)
            for data in response['statuses']:
                comments_count = data['comments_count']
                if comments_count != 0:
                    soup = BeautifulSoup(data['text'], 'lxml')
                    content = soup.get_text()
                    idstr = data['idstr']
                    uid_str = data['user']['idstr']
                    print('content:{}---comments_count:{}---idstr:{}---uid:{}'.format(content, comments_count, idstr,
                                                                                      uid_str))
                    resp = requests.get('https://weibo.com/ajax/statuses/buildComments?',
                                        params={
                                            "is_reload": "1",
                                            "id": "{}".format(idstr),
                                            "is_show_bulletin": "2",
                                            "is_mix": "0",
                                            "count": "20",
                                            "type": "feed",
                                            "uid": "{}".format(uid_str),
                                            "fetch_level": "0"
                                        }, headers=headers, cookies=cookies).json()
                    for datas in resp['data']:
                        sp = BeautifulSoup(datas['text'], 'lxml')
                        comment = sp.get_text()
                        if key_words in comment:
                            print('contain_comment:', comment)
                            comment_name = datas['user']['screen_name']
                            comment_id = datas['user']['id']
                            comment_location = datas['user']['location']
                            comment_followers_count = datas['user']['followers_count']
                            comment_description = datas['user']['description']
                            collection.update_one({'content': content, 'comment': comment, 'comment_id': comment_id},
                                                  {'$set': {'content': content,
                                                            'comment': comment,
                                                            'comment_id': comment_id,
                                                            'comment_name': comment_name,
                                                            'comment_location': comment_location,
                                                            'comment_followers_count': comment_followers_count,
                                                            'comment_description': comment_description}}, True)
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)

        except (KeyError, json.JSONDecodeError) as e:
            print("数据解析异常:", e)

        except Exception as e:
            print("其他异常:", e)


if __name__ == '__main__':
    scrape_index('歧视')
