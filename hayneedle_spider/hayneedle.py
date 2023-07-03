import csv
import time

import requests

cookies = {
    'SSLB': '1',
    'x-instart-ogn': 'sslb',
    'SSID': 'CQD5Ax0OAAAAAACJ249kXqNADonbj2QBAAAAAAAAAAAAiduPZADe0CInAQGkeSUAiduPZAEA',
    'SSSC': '631.G7246251707158537054.1|75554.2455972',
    'BRAND_SID': '1CFC7840-1A43-4349-A7C74B73E0D31339',
    'SID': 'FD59526B-CD4F-4426-9A5B316906D992E3',
    'GLOBAL_SID': 'EEFE3D3E-D022-442A-AB8417EADBF877ED',
    'SIGNATURE': 'MOP1ZEymOvorRyeh90BH2H9rbOH5xvOho2TDDNQT9uXCoKGYLpefteUuu%2BX7YJzJ',
    'SESSION_COUNTER': '3885535121',
    'SITE_ID': '669',
    'GEO_DATA': "<wddxPacket%20version='1.0'><header/><data><struct><var%20name='COUNTRY'><string>US</string></var><var%20name='POSTAL_CODE'><string>97818</string></var><var%20name='STATE'><string>OR</string></var><var%20name='CITY'><string>BOARDMAN</string></var></struct></data></wddxPacket>",
    'NAVIGATION_PATH': 'CATEGORY%3A169309%2CCATEGORY%3A183824%2CCATEGORY%3A187788',
    'GLOBAL_CUSTOMER_ACCOUNT': "<wddxPacket%20version='1.0'></wddxPacket><header/><data><struct><var%20name='SIGNED_IN'><string>N</string></var><var%20name='CUSTOMER_ID'><string>0</string></var><var%20name='CUSTOMER_FIRST_NAME'><string></string></var></struct></data></wddxPacket>",
    'rxVisitor': '1687149460406J968G195HVQ3P7M8EJ23NQQHLFMPR0PG',
    'dtCookie': 'v_4_srv_70_sn_TQ19EBRCSLLGO49R7KOIVQ7UK3PUG6L3_app-3Aa72d29e05914fd9a_1_ol_0_perc_100000_mul_1',
    'dtLatC': '1',
    'dtSa': '-',
    'SSRT': '7duPZAADAA',
    'x-csrf-jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiYmUzNWY0YTMtZmY3NS00N2FjLWI0MzUtNWRkOGRjMzc5ODFiIiwidHlwZSI6ImNvb2tpZSIsImlhdCI6MTY4NzE0OTU1MH0.knW6r-WjfFYsM_3Qnja0WiVe1k6cXog606Zin0Vi_lk',
    '_pxhd': 'HjC9vyUMFvPKeizyHQWOVUwfiMfVbZFqpE20436K0swFWZ3VhXqL4gp1dLLKJngaNCjHjK9CFbbG/Pa-yYDgoQ==:IeIhTbkCVmHKRmXkakMj2HSinoS80InDk4-q5IDWO6nvcYAYqY8GDX/dMT/jFqpvWAeuxU7s5mzWFI8d2SRBHiEoveyOng3S-2aaT5J0axs=',
    'TS01ada97e': '01138a503214e166406a6d94ecb29ae05ac0a0f87ceec4c35a5a076e7e713dddd0d11c007c11fb40d6c2cd69c12bde65709a2f8c0e38424b6fb8d65d0254f5c2d8093dad15663e927833139f86afba69b0387698874b9f1b044c722afa0610c8ed5e16e5a101deb0e5aa5dd8fb332cfa1383789945a9476b69f50d0ee52c97a2f0b9869f3171fa6d592639fc92f80c10102581980c5d515b7482f1533ad2e3fb95f58411c65eb1fae258a3e14f183db9db62c7d37dd0c8706b7f337134e92155722df5a733b737fee83eb8122881ec323cd4e7d0fcf5a4c90bafe0e83418647a1ae8fa817d',
    'rxvt': '1687151377341|1687149460407',
    'dtPC': '70$549508081_984h8vFHHVWMWGIVWKUWJAECDPRKCWJLEHEIAH-0e0',
}

headers = {
    'authority': 'www.hayneedle.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'cookie': "SSLB=1; x-instart-ogn=sslb; SSID=CQD5Ax0OAAAAAACJ249kXqNADonbj2QBAAAAAAAAAAAAiduPZADe0CInAQGkeSUAiduPZAEA; SSSC=631.G7246251707158537054.1|75554.2455972; BRAND_SID=1CFC7840-1A43-4349-A7C74B73E0D31339; SID=FD59526B-CD4F-4426-9A5B316906D992E3; GLOBAL_SID=EEFE3D3E-D022-442A-AB8417EADBF877ED; SIGNATURE=MOP1ZEymOvorRyeh90BH2H9rbOH5xvOho2TDDNQT9uXCoKGYLpefteUuu%2BX7YJzJ; SESSION_COUNTER=3885535121; SITE_ID=669; GEO_DATA=<wddxPacket%20version='1.0'><header/><data><struct><var%20name='COUNTRY'><string>US</string></var><var%20name='POSTAL_CODE'><string>97818</string></var><var%20name='STATE'><string>OR</string></var><var%20name='CITY'><string>BOARDMAN</string></var></struct></data></wddxPacket>; NAVIGATION_PATH=CATEGORY%3A169309%2CCATEGORY%3A183824%2CCATEGORY%3A187788; GLOBAL_CUSTOMER_ACCOUNT=<wddxPacket%20version='1.0'></wddxPacket><header/><data><struct><var%20name='SIGNED_IN'><string>N</string></var><var%20name='CUSTOMER_ID'><string>0</string></var><var%20name='CUSTOMER_FIRST_NAME'><string></string></var></struct></data></wddxPacket>; rxVisitor=1687149460406J968G195HVQ3P7M8EJ23NQQHLFMPR0PG; dtCookie=v_4_srv_70_sn_TQ19EBRCSLLGO49R7KOIVQ7UK3PUG6L3_app-3Aa72d29e05914fd9a_1_ol_0_perc_100000_mul_1; dtLatC=1; dtSa=-; SSRT=7duPZAADAA; x-csrf-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiYmUzNWY0YTMtZmY3NS00N2FjLWI0MzUtNWRkOGRjMzc5ODFiIiwidHlwZSI6ImNvb2tpZSIsImlhdCI6MTY4NzE0OTU1MH0.knW6r-WjfFYsM_3Qnja0WiVe1k6cXog606Zin0Vi_lk; _pxhd=HjC9vyUMFvPKeizyHQWOVUwfiMfVbZFqpE20436K0swFWZ3VhXqL4gp1dLLKJngaNCjHjK9CFbbG/Pa-yYDgoQ==:IeIhTbkCVmHKRmXkakMj2HSinoS80InDk4-q5IDWO6nvcYAYqY8GDX/dMT/jFqpvWAeuxU7s5mzWFI8d2SRBHiEoveyOng3S-2aaT5J0axs=; TS01ada97e=01138a503214e166406a6d94ecb29ae05ac0a0f87ceec4c35a5a076e7e713dddd0d11c007c11fb40d6c2cd69c12bde65709a2f8c0e38424b6fb8d65d0254f5c2d8093dad15663e927833139f86afba69b0387698874b9f1b044c722afa0610c8ed5e16e5a101deb0e5aa5dd8fb332cfa1383789945a9476b69f50d0ee52c97a2f0b9869f3171fa6d592639fc92f80c10102581980c5d515b7482f1533ad2e3fb95f58411c65eb1fae258a3e14f183db9db62c7d37dd0c8706b7f337134e92155722df5a733b737fee83eb8122881ec323cd4e7d0fcf5a4c90bafe0e83418647a1ae8fa817d; rxvt=1687151377341|1687149460407; dtPC=70$549508081_984h8vFHHVWMWGIVWKUWJAECDPRKCWJLEHEIAH-0e0",
    'referer': 'https://www.hayneedle.com/furniture/desks_list_187788?categoryID=187788&page=3&searchQuery=&selectedFacets=139%3D30006&sortBy=',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-dtpc': '70$549508081_984h8vFHHVWMWGIVWKUWJAECDPRKCWJLEHEIAH-0e0',
    'x-dtreferer': 'https://www.hayneedle.com/furniture/desks_list_187788?categoryID=187788&page=2&searchQuery=&selectedFacets=139%3D30006&sortBy=',
}

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for page in range(1, 21):
        print('scraping page:', page)
        params = {
            'INTERPRETATION_ID': '',
            'arriveInTimeSelectedFlag': 'false',
            'categoryID': '187788',
            'contentCardIndex': '22',
            'currentSku': '',
            'facetBanner': '',
            'hasBlogCard': 'false',
            'hasContentCard': 'true',
            'isExtendedCardLimitExperiment': 'false',
            'isMobileResultListExperiment': 'false',
            'isSearchPage': 'false',
            'page': f'{page}',
            'pageType': 'noFilter',
            'primaryCategoryName': '',
            'resultListCardTotal': '934',
            'searchQuery': '',
            'selectedFacets': '139=30006',
            'sortBy': '',
            'viewAll': 'false',
        }

        response = requests.get(
            'https://www.hayneedle.com/sf-service/resultList/getResultList',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        print(response.status_code)
        jsons = response.json()
        for item in jsons['cardsArray']:
            url_list = []
            name = item['name']
            for i in item['images']:
                url_list.append(i['url'])

            writer.writerow({'Name': name, 'URL': url_list})

        time.sleep(1.5)
