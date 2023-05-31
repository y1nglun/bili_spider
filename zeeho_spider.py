import requests
import pandas as pd

url = 'https://www.zeehoev.com/cfmotoserverevow/ow/afterSale/listStoreByCondition?key=&provinceCode=&cityCode=&latitude=39.850173&longitude=116.37748&networkType=2'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36"
}

df = pd.DataFrame(columns=['Name', 'Phone', 'Address'])

response = requests.get(url, headers=headers).json()
for data in response['data']:
    name = data['storeName']
    phone = data['contactPhone']
    address = data['address']
    print('name:{}---phone:{}---address:{}'.format(name, phone, address))
    row = {'Name': name, 'Phone': phone, 'Address': address}
    df = pd.concat([df, pd.DataFrame([row])])

df.to_excel('output.xlsx', index=False)
