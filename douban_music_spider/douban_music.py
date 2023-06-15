import requests
from bs4 import BeautifulSoup
import pymysql

TOTAL_PAGE = 10
host = 'localhost'
user = ''
password = ''
database = 'douban'
table = 'music_top250'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}
cookie = 'll="108288"; bid=Z_3vBiV0kFs; douban-fav-remind=1; __utma=30149280.1241984296.1685431973.1685431973.1685431973.1; __utmz=30149280.1685431973.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="186160890:EjnkiO9pknM"; push_noty_num=0; push_doumail_num=0; ct=y; ck=i5eL; ap_v=0,6.0; frodotk_db="cdd05f1bf6b0628569711d53e411278f"; _pk_ref.100001.afe6=%5B%22%22%2C%22%22%2C1686300802%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DpRFI47TQshNvuyhsXaR6q8lCy1VtH6iwBb4HWE7ZRdiP-I8-Kn167Ou5npMZsrno%26wd%3D%26eqid%3De46fb54600001714000000026482e013%22%5D; __yadk_uid=qZGlMPVM48dXrPNOEy1BqSfSHYz5FQyf; _vwo_uuid_v2=D004B5219D91B7D1A911BD2AE7E6085FF|99baf14ce9a31d992d99efc3ce298832; _pk_ses.100001.afe6=*; _pk_id.100001.afe6=23fa16787812ebe8.1686298647..1686304462.undefined.'


def save(title, author, link, score, introduce):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        link VARCHAR(255),
        score VARCHAR(255),
        introduce TEXT
    )
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)

        sql = f"INSERT INTO {table} (title, author, link, score, introduce) VALUES (%s, %s, %s, %s, %s) " \
              f"ON DUPLICATE KEY UPDATE author=VALUES(author), link=VALUES(link), score=VALUES(score), " \
              f"introduce=VALUES(introduce)"
        values = (title, author, link, score, introduce)
        cursor.execute(sql, values)

    conn.commit()
    conn.close()


for page in range(0, TOTAL_PAGE * 25, 25):
    url = f'https://music.douban.com/top250?start={page}'
    print(f'scraping url: {url}')
    response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
    soup = BeautifulSoup(response.text, 'lxml')
    for item in soup.select('div[class="indent"] table'):
        link = item.select_one('.nbg')['href'].strip()
        title = item.select_one('.pl2 a').get_text(strip=True)
        score = item.select_one('.rating_nums').get_text()
        author = item.select_one('.pl2 .pl').get_text(strip=True).split('/')[0]
        print(f'scraping url: {link}')
        response = requests.get(link, headers=headers, cookies={'Cookie': cookie})
        soup = BeautifulSoup(response.text, 'lxml')
        introduce_element = soup.select_one('span[property="v:summary"]')
        introduce = introduce_element.get_text(strip=True) if introduce_element else ''
        save(title, author, link, score, introduce)

print('Finished scraping and saving data.')
