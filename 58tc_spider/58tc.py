import time

import requests
from bs4 import BeautifulSoup
import csv

cookies = 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; SECKEY_ABVK=Qi4K9s8Mhxn3oFc1Q4o6jp7Yu3yk+3CINTUgRIvxnZE%3D; BMAP_SECKEY=W9OqEq2Xwy40Y69kzdAGralpVRa7-txuMUqWiIlqoDPkaPEA-De2U2m1trUt52uLLKUqwEfo_NthfsSoRlPSBe3B8tbRljfmoB81OPMQBab3tj3pVgvsIzA0A2WR_YeXOZ4kYuA0woYaI4ueG6IHih7uBJ6uIqrIbJebahIvEEh7owkV2YGjJ4l2rzVO0JoF; myLat=""; myLon=""; id58=CNF/XmSL/lwW6cSyI7gF4Q==; mcity=bj; f=n; city=bj; 58home=bj; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; 58tj_uuid=0aefd71d-49ba-4cca-8813-5226e432a7af; new_uv=1; utm_source=market; spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.K600000eqeDrETZJhwvoo38gRABJLYUM9p0600fsUaL4g27nzJBUfk4BN3lsD7UOC_ePxxd8DyywXwHbKjNaYLfnkwwB9adT75zfDG7Ebgeraf3UhCvMNWJh0wcUUYimerdHxExuRnxjjXDe7Tx7MutNiqn8z0X0UxWZztvh6Rz3Rx7jES-j7MpJv5zuWZB3CpVHqSlOdbcXGQVNgslQRvqSNjrC.DY_NR2Ar5Od66z3PrrW6ButVvkDj3n-vHwYxw_vU85YIMAQV8qhORGyAp7WIu8L6.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPHWPoQ5Z0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5HR31pz1ksKzmLmqn0KdThkxpyfqnHRYPHc4nj6srfKVINqGujYkPHcdPWn4P0KVgv-b5HDznHf1n1Dv0AdYTAkxpyfqnHc3nWm0TZuxpyfqn0KGuAnqiDF70ZKGujYk0APGujY1rjn0mLFW5HDsrjf4%2526dt%253D1686896218%2526wd%253D58%2525E5%25259; xxzl_cid=e98156f536494853b9f72d6575e716ab; xxzl_deviceid=uvfGjFJlg2SnwOcwUCRGeoxe3xps7RoW3IBasfYVqgUsuL6IGc4LerNR2jOrr0yO; als=0; wmda_uuid=441a93f45c7fe9c49544d03c6303febc; wmda_new_uuid=1; wmda_session_id_11187958619315=1686896223303-ff98d8ef-1a9d-ad4b; sessionid=1751c90b-9c40-4d16-a77a-78dccfecb535; fzq_h=ccc85886681fe92d1675fda640b01a00_1686896266660_fd185e9bcc7c418c8922b44c48a6944f_1928741006; new_session=0; wmda_session_id_1731916484865=1686896268040-2dfb5d72-08ed-4912; wmda_visited_projects=%3B11187958619315%3B1731916484865; jobBottomBar=1; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1686896273; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1686897921; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1686897962; JSESSIONID=A391FEEA25860632B38906C5125D451E; fzq_js_zhaopin_list_pc=c4b4f0b10f7a7cb5e6d069b1169ce7d9_1686898222059_7; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1686898222; crmvip=; dk_cookie=; PPU=UID=57144252584727&UN=5k4st78qc&TT=e12bd90b7ff2bbffc5f4361da7dc3faa&PBODY=TIxdnNRVuYIGYeXo4eSmT2TBTRo9JlgexN6BcGT3ESW3A6WRam91g-54Jg4Y4Po71LBLLsw5KMEaJxqIsY4jbqB_JTWHg11XI3LR7zI8QMt5x9YMuNFmLpekwKYIvXcA7rn_KJXR78PhXVs9uSEt8vWYQgBG82XVegwSUkb3H2M&VER=1&CUID=h19B8A9Mg-7T-9umZfA-Rw; www58com=UserID=57144252584727&UserName=5k4st78qc; 58cooper=userid=57144252584727&username=5k4st78qc; 58uname=5k4st78qc; passportAccount=atype=0&bstate=0; fzq_js_infodetailweb=821e4c3b69f8f2397bdbc808585414d3_1686898631370_9; PPU.sig=7XWyDAZ2CCwtB3V09XhzneyZMQk; ppStore_fingerprint=A556ACB720A17458EEB0EBCC626C16C59E80DC1DB64E9F38%EF%BC%BF1686898632420'

headers = {
    'authority': 'bj.58.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; userid360_xml=DE09EA5C90CEC1CC0294588512650262; time_create=1689488273848; myLat=""; myLon=""; id58=CNF/XmSL/lwW6cSyI7gF4Q==; mcity=bj; f=n; city=bj; 58home=bj; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; 58tj_uuid=0aefd71d-49ba-4cca-8813-5226e432a7af; new_uv=1; utm_source=market; spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.K600000eqeDrETZJhwvoo38gRABJLYUM9p0600fsUaL4g27nzJBUfk4BN3lsD7UOC_ePxxd8DyywXwHbKjNaYLfnkwwB9adT75zfDG7Ebgeraf3UhCvMNWJh0wcUUYimerdHxExuRnxjjXDe7Tx7MutNiqn8z0X0UxWZztvh6Rz3Rx7jES-j7MpJv5zuWZB3CpVHqSlOdbcXGQVNgslQRvqSNjrC.DY_NR2Ar5Od66z3PrrW6ButVvkDj3n-vHwYxw_vU85YIMAQV8qhORGyAp7WIu8L6.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPHWPoQ5Z0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5HR31pz1ksKzmLmqn0KdThkxpyfqnHRYPHc4nj6srfKVINqGujYkPHcdPWn4P0KVgv-b5HDznHf1n1Dv0AdYTAkxpyfqnHc3nWm0TZuxpyfqn0KGuAnqiDF70ZKGujYk0APGujY1rjn0mLFW5HDsrjf4%2526dt%253D1686896218%2526wd%253D58%2525E5%25259; xxzl_cid=e98156f536494853b9f72d6575e716ab; xxzl_deviceid=uvfGjFJlg2SnwOcwUCRGeoxe3xps7RoW3IBasfYVqgUsuL6IGc4LerNR2jOrr0yO; als=0; wmda_uuid=441a93f45c7fe9c49544d03c6303febc; wmda_new_uuid=1; wmda_session_id_11187958619315=1686896223303-ff98d8ef-1a9d-ad4b; sessionid=1751c90b-9c40-4d16-a77a-78dccfecb535; fzq_h=ccc85886681fe92d1675fda640b01a00_1686896266660_fd185e9bcc7c418c8922b44c48a6944f_1928741006; new_session=0; wmda_session_id_1731916484865=1686896268040-2dfb5d72-08ed-4912; wmda_visited_projects=%3B11187958619315%3B1731916484865; jobBottomBar=1; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1686896273; JSESSIONID=AF938452A3262C758A321A4BFC0EA102; fzq_js_zhaopin_list_pc=a30379a398c645831789b35adb3768cd_1686896671361_6; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1686896671',
    'referer': 'https://bj.58.com/pugongjg/pn5/?fullPath=674,413249&pid=568440114638422016&PGTID=0d364e41-0000-138e-ad50-fe3a605d6dd9&ClickID=3',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

with open('jobs.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Address', 'Name', 'Salary', 'Category', 'Education', 'Experience', 'Company Name', 'Description'])

    for page in range(1, 20):
        url = f'https://bj.58.com/pugongjg/pn{page}/?fullPath=674,413249&pid=568440114638422016&PGTID=0d364e41-0000-128f-b237-b7dc51ebeb6e&ClickID=3'
        print('scraping:', url)
        response = requests.get(url, cookies={'Cookie': cookies}, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        for item in soup.select('.job_item'):
            address = item.select_one('.address').get_text().strip()
            name = item.select_one('.name').get_text().strip()
            salary = item.select_one('.job_salary').get_text().strip()
            cate = item.select_one('.job_require .cate').get_text().strip()
            xueli = item.select_one('.job_require .xueli').get_text().strip()
            jingyan = item.select_one('.job_require .jingyan').get_text().strip()
            comp_name = item.select_one('.comp_name a').get_text().strip()
            link = item.select_one('.job_name a')['href']
            print(address, name, salary, cate, xueli, jingyan, comp_name)
            response = requests.get(link, headers=headers, cookies={'Cookie': cookies})
            print('scraping detail:', link)
            soup = BeautifulSoup(response.text, 'lxml')
            des_match = soup.select_one('.des')
            if des_match:
                des = des_match.get_text().strip()
            else:
                des = ''

            writer.writerow([address, name, salary, cate, xueli, jingyan, comp_name, des])
        time.sleep(1.5)
