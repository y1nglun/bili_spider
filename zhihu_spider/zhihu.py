import time
import csv
import requests
from bs4 import BeautifulSoup

# import pymongo

# 需修改,填写自己Cookie值
COOKIE = '_zap=51a97d79-3728-4dac-803c-4f74e5277896; d_c0=ABAYvQm7jhaPTtfjzxxKP28zLBvEzfmGlME=|1680315611; _xsrf=K4WcCtQSScCBZ6ETMGaSsCyLYfd2gasR; __snaker__id=cbUpu6mgwWLl7nhm; YD00517437729195%3AWM_TID=uInyGSrYAYtBRQQFRUaQbzz%2Bz5Cwh5TU; q_c1=a30b2a86f70c4587a1b5429ad45ad8ac|1681207818000|1681207818000; YD00517437729195%3AWM_NI=fX0pRgNRAaRjuIBdj9nsewQAHo0HGmBsBXCTzSnAII3bJZ7m%2BgLUiIA8hE9lnAKoy5C4nAjpjSGM3OQ5n%2FVh1AtgEZArOAJLgtI1fUpKA87smPUhh0mVwa25mCAZf63tRzQ%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee98f745f1a886a4b66a87eb8bb2c84b929a8badc43c98efbaa8e5218ab6a1d0b32af0fea7c3b92aa6880091d16d8e8e8f82d162b7978e85e933aeadab98d44b8cb100a9c66782ad8eb9c260ba8da2a2cc43f1be86bbb667e9b984b6ec4383e8a8a6bc68ae9f8590fc3f81eca2a2e97caa8d89aeb24593eba2d0d564f39fbc88c85283ae81a2c948a5ac87d2e55fb4958fd9b679af909b89eb3caf8ab982b13faf9d8fbbe53ef1ac9e9bd437e2a3; gdxidpyhxdE=Y4zgc1CdxY0qSbY9Ajf4nSu6Ko9uvB86tpt0%2FasHVHCQ9R%2BXoATul%2FiGT519eBsZTBbjUtiImTDZ1hnXOhnPqNvP%5C2l6BRg48SlH4CqXvisHbXMfjl05l%5C9%2Btq02n9l%5Cq0lAfBR4yfkgUY3q1DpuUWMT%2FSlJbqvs3et%5C3HPii5Q4c7sp%3A1685411636543; captcha_session_v2=2|1:0|10:1685410736|18:captcha_session_v2|88:akpRSTZWdHpBWVpUSzVyTklmeG1icWhUeGtoZXhTNUlqdS9MSlJvRDZyR0RrZi8vRTlDaHAzeGFmWTdaY3J3Qg==|107ad9b808c2b78671580a898263b211c61fc0539449906fcacd3c5668953605; captcha_ticket_v2=2|1:0|10:1685411205|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfVXBRaGNOLkU4Q0NsYXljUTd1QlFQelZVbUxlajc2U2dyaC5KaUsxdzc1QmF4OC5UY25IZWhqN3R4cVdaREFFRVJvcmFRNEg2NUkyRHhmenI1UlZxSkliZkZXSTJJandzcG1MdGhVVjQyc3FlYkxUaGVLLW9EWkQ4S2ZKYS4ycUdib0JtdVlrWU5CLTk1ZFBkVmdrQTBMRFN0UWRoMnkxak9YOVNZaWZDb0FsczYudURySjRRMXJjcWpwbC0wZHB2OWpMdFlKNDhvTVN4MWw0VW1QY285TkVDU1JTbHJKN3NPSWdLYTQueTJra3BMUVliYnRPNzhPMjZBYzJuTHcxVEZwZDZBb1NJOHA5eXVMODlkak8yUm96cEdlRTlsNTR1WUg0b3ZhSzguRWdYSFh3Z2hpVmFLMHlrUEtKSGs0VmVZOVJ6ckk2empIVHlxaHExQVdIVXVTdFRPaV9rZnlWZXNHMXM4emVmVUdLQm5BSTJMT2tLWjdmSjFqNnpPdDVGQVZTTG02YUdwTThKQnpDZnpkQ0xxbUFnWEJ1dE1oUFVxSXNBY1c5ZGxEbGhMU2tjMkktWXZRbl9hNGUuYTRMczZtRm90U0YtNE4wbF81bUxjMW5aMFlEUGNlZGVlaDE4dEZ3Mi1ESUVRZ0ZhbE5SZGVDVWYwRW43V3NjMyJ9|a247783118c7f91d01af4a199131587ef64b3757337c99591b9ba8218f7ddacc; z_c0=2|1:0|10:1685411207|4:z_c0|92:Mi4xR3lkb0JRQUFBQUFBRUJpOUNidU9GaVlBQUFCZ0FsVk5oNk5pWlFDMnRVOEt1TkxnQjhYZWRXbWl4UEFhZHpLOUhB|89a90df85ef1dbd2e42072f020c9f8e85c71d9fdf348f8180a8d85b1dcd29e0f; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1683350783,1685364606,1685410210,1685538628; tst=r; SESSIONID=JSm8zl6xeNY2mci3jLaW60iFSc215vZ9Qj4L5yeJPvV; JOID=W1EVCkoTMJTdgzSOWhNIhP5fNRpFWWrw7fFYsSt-fsTm5l_nYB2_7LmLPY5byMjRoaM64zvWMEvYp0T6NLX8ObE=; osd=V1wUAEsfPZXXgjiDWxlJiPNePxtJVGv67P1VsCF_csnn7F7rbRy17bWGPIRaxMXQq6I27jrcMUfVpk77OLj9M7A=; KLBRSID=c450def82e5863a200934bb67541d696|1685688106|1685688049'  # 手动登录,获取cookie
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
url = 'https://www.zhihu.com/api/v4/questions/33870165/feeds?cursor=545d248f25074ac8b935a400faeb2785&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id=1686637661864137036'
is_end = False

with open('protect_eyes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'gender', 'follower_count', 'headline', 'avatar_url', 'like', 'content'])

    while not is_end:
        response = requests.get(url, headers=headers, cookies={'Cookie': COOKIE}).json()
        is_end = response['paging']['is_end']
        for data in response['data']:
            content = data['target']['content']
            soup = BeautifulSoup(content, 'lxml')
            line = soup.get_text()
            name = data['target']['author']['name']
            voteup_count = data['target']['voteup_count']
            avatar_url = data['target']['author']['avatar_url']
            follower_count = data['target']['author']['follower_count']
            gender = data['target']['author']['gender']
            headline = data['target']['author']['headline']
            writer.writerow([name, gender, follower_count, headline, avatar_url, voteup_count, line])
            print(
                f'name:{name} -*-gender:{gender}-*-follower:{follower_count}-*-headline:{headline}-*- like:{voteup_count} -*- content:{line}')

        url = response['paging']['next']
        time.sleep(2)

print('spider finished')
