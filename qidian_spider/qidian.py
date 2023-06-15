import re
import requests
from fontTools.ttLib import TTFont
from lxml import etree
import csv


def get_book_name(xml_obj):
    name_list = xml_obj.xpath('//*[@id="book-img-text"]/ul/li/div/h2/a/text()')
    return name_list


def get_author(xml_obj):
    author_list = xml_obj.xpath('//*[@id="book-img-text"]/ul/li/div[2]/p[1]/a[1]/text()')
    return author_list


def get_yuepiao(str_data):
    yuepiao_list = re.findall(r'''</style><span class=".*?">(.*?)</span>''', str_data)
    return yuepiao_list


def get_font(xml_obj, headers_):
    font_div = xml_obj.xpath("//span/style/text()")[0]
    font_url = re.findall("eot.*?(https:.*?.woff)", font_div)[0]
    font_name = str(font_url).rsplit('/', 1)[1]
    # 获取font文件进行本地保存
    font_data = requests.get(font_url, headers_).content
    with open(f'{font_name}', 'wb') as f:
        f.write(font_data)
    # 加载字体文件
    font_data = TTFont(f'{font_name}')
    # font_data.saveXML('字体.xml')
    font_doct01 = font_data.getBestCmap()
    font_doct02 = {
        'period': '.',
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'

    }
    for i in font_doct01:
        font_doct01[i] = font_doct02[font_doct01[i]]
    return font_doct01


def jiemi(miwen_list, font_list):
    yuepiao = []
    for i in miwen_list:
        num = ''
        mw_list = re.findall('&#(.*?);', i)

        for j in mw_list:
            num += font_list[int(j)]
        yuepiao.append(int(num))
    return yuepiao


if __name__ == '__main__':

    headers_ = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'referer': 'https://www.qidian.com/rank/',
        'cookie': 'e1=%7B%22pid%22%3A%22qd_P_rank_19%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A5%7D; e2=%7B%22pid%22%3A%22qd_P_rank_19%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A5%7D; _yep_uuid=6a2ad124-678f-04d3-7195-2e4e9f5c470e; _gid=GA1.2.501012674.1638335311; newstatisticUUID=1638335311_1217304635; _csrfToken=adBfL5dzru0KuzVgLJpxtsE8zQcfgZT8MzKf0aMs; e2=; e1=%7B%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A16%22%2C%22l1%22%3A3%7D; _ga_FZMMH98S83=GS1.1.1638362844.2.1.1638362855.0; _ga_PFYW0QLV3P=GS1.1.1638362844.2.1.1638362855.0; _ga=GA1.2.2025243050.1638335311; _gat_gtag_UA_199934072_2=1'
    }
    url_ = 'https://www.qidian.com/rank/yuepiao/'

    str_data = requests.get(url_, headers=headers_).text

    xml_obj = etree.HTML(str_data)
    book_name_list = get_book_name(xml_obj)
    author_name_list = get_author(xml_obj)

    yuepiao_list = jiemi(get_yuepiao(str_data), get_font(xml_obj, headers_))
    for i in range(len(book_name_list)):
        print(f'{book_name_list[i]}:{author_name_list[i]}:{yuepiao_list[i]}')

    with open('data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['书名', '作者', '月票'])
        for i in range(len(book_name_list)):
            writer.writerow([book_name_list[i], author_name_list[i], yuepiao_list[i]])
