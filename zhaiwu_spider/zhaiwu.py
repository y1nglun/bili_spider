import requests
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from urllib.parse import urljoin, quote, urlencode

cookies = {
    'JSESSIONID': 'CDE737D1ED78A0BCCE2C9AD64B3FD626',
    'BIGipServerPool_tomcat-cmsFe_80': '!EgqCDduxSQzyrbXhbVl+9jfiAfP8U8a4QcCsGZkn3UwbEzAkTOJ0G7z7SqLaTsLzwWK6vRGFB9SiMgc=',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=CDE737D1ED78A0BCCE2C9AD64B3FD626; BIGipServerPool_tomcat-cmsFe_80=!EgqCDduxSQzyrbXhbVl+9jfiAfP8U8a4QcCsGZkn3UwbEzAkTOJ0G7z7SqLaTsLzwWK6vRGFB9SiMgc=',
    'Referer': 'https://www.chinabond.com.cn/dfz/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
# 电子邮件参数
sender_email = "1149587364@qq.com"
receiver_email = "y1nglun0911@gmail.com"
smtp_server = "smtp.qq.com"
smtp_port = 465
email_password = "lemhcibshmdpiaeb"

# 关键词和公告列表
keyword = "披露"
announcements = []


# 发送邮件
def send_email():
    print('start send email')
    if announcements:
        subject = "新公告通知"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = Header(subject, "utf-8")

        # 构造邮件正文
        body = "以下是包含关键词“{}”的新公告：\n\n".format(keyword)
        for announcement in announcements:
            body += announcement + "\n"
        message.attach(MIMEText(body, "plain", "utf-8"))

        # 连接到SMTP服务器并发送邮件
        try:
            smtp_obj = SMTP_SSL(smtp_server, smtp_port)
            smtp_obj.login(sender_email, email_password)
            smtp_obj.sendmail(sender_email, receiver_email, message.as_string())
            smtp_obj.quit()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败:", str(e))


# 爬取网页并查找新公告
def crawl_website():
    print('start crawling')
    url = "https://www.chinabond.com.cn/lgb/infoListByPath"
    params = {
        '_tp_lgbInfo': '1',
        'pageSize': '10',
        'channelPath': 'ROOT>业务操作>发行与付息兑付>债券种类>地方债信息披露>信息披露文件',
        'issuer': '',
        'depth': '2',
        't': '1687146547461',
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
    for item in response['lgbInfoList']:
        title = item['title']
        if keyword in title:
            print(title)
            base_url = 'https://www.chinabond.com.cn/dfz/#/information/listDetail?'
            encoded_title = quote(title)
            encoded_name = quote('全部')
            announcement_url = base_url + f'title={encoded_title}&id={item["id"]}&time={item["createTime"]}&name={encoded_name}'
            if announcement_url not in announcements:
                print(announcement_url)
                announcements.append(announcement_url)

    send_email()


# 设置定时任务
scheduler = BlockingScheduler()
scheduler.add_job(crawl_website, "interval", minutes=10, next_run_time=datetime.now())
scheduler.add_job(send_email, "interval", minutes=30)
scheduler.start()
