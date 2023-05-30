import time

import requests
from bs4 import BeautifulSoup
import pymongo

COOKIE = ''  # 手动登录,获取cookie
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Referer': 'https://www.zhihu.com/'
}
# params = {
#     "cursor": "21bf0a72ab8f37e926eba14d15976d75",
#     "include": "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled",
#     "limit": "5",
#     "offset": "0",
#     "order": "default",
#     "platform": "desktop",
#     "session_id": "1685418098316824630"
# }

# 根据个人需要,填写问题链接,之后根据返回next_url自动爬取
url = 'https://www.zhihu.com/api/v4/questions/38915323/feeds?cursor=5932e24c3a0f2239e94a2afe16ae6532&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1685422395849511896'

is_end = False

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['zhihu']
collection = db['question']

while not is_end:
    response = requests.get(url, headers=headers, cookies={'Cookie': COOKIE}).json()
    is_end = response['paging']['is_end']
    for data in response['data']:
        content = data['target']['content']
        soup = BeautifulSoup(content, 'lxml')
        line = soup.get_text()
        name = data['target']['author']['name']
        voteup_count = data['target']['voteup_count']
        print('name:{} -*- like:{} -*- content:{}'.format(name, voteup_count, line))
        collection.update_one({'name': name, 'like': voteup_count, 'content': line},
                              {'$set': {'name': name, 'like': voteup_count, 'content': line}}, True)
    url = response['paging']['next']
    time.sleep(2)

print('spider finished')
