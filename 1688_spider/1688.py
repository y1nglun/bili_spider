import time
import execjs
import requests

token = '850c6199fe5b4b0a5f812fd080f805f7'
i = round(time.time() * 1000)
g = '12574478'
data = '{"cid":"TpFacRecommendService:TpFacRecommendService","methodName":"execute","params":"{\\"pageNo\\":\\"1\\",\\"cna\\":\\"bdCrHGAC/FkCAd3cZuiGIm7/\\",\\"pageSize\\":\\"20\\",\\"from\\":\\"PC\\",\\"sort\\":\\"mix\\",\\"trafficSource\\":\\"pc_index_recommend\\"}"}'

signKey = token + "&" + str(i) + "&" + g + "&" + data
with open('./1688.js', 'r', encoding='utf-8') as f:
    jscode = f.read()

ctx = execjs.compile(jscode).call('h', signKey)
print(ctx)

params = {
    'jsv': '2.6.1',
    'appKey': '12574478',
    't': i,
    'sign': ctx,
    'v': '1.0',
    'type': 'jsonp',
    'isSec': 0,
    'timeout': 20000,
    'api': 'mtop.taobao.widgetService.getJsonComponent',
    'dataType': 'jsonp',
    'jsonpIncPrefix': 'mboxfc',
    'callback': 'mtopjsonpmboxfc9',
    'data': data
}

url = 'https://h5api.m.1688.com/h5/mtop.taobao.widgetservice.getjsoncomponent/1.0/?'
headers = {
    'refer': 'https://sale.1688.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'cookie': '_m_h5_tk=850c6199fe5b4b0a5f812fd080f805f7_1686025659505; _m_h5_tk_enc=6d164676c72bd5f36313ea22603ace94; sgcookie=E100GSfnVRScQRN2Krt%2Fud0h4pfnHanKx%2BwN5aL9boFb2kxdAL4NYijJtZexzIGIJyVikz4d7QjbrX1sPb%2FVoBx28jGizb012VYgNiMKgVWS6D8%3D; t=32aa5bba1ed604e52eb1c987d3813ffc; lid=t_1478697461711_0; uc4=id4=0%40UgcnD5UDeany7kbZ8hLhw4xu5leG&nk4=0%40FbMocpOBNLIb%2FQ7GOIpzLNixePpfPUB08TrK4g%3D%3D; __cn_logon__=false; cookie2=19db2d59a5f98bb0326b31ad79b1865d; _tb_token_=36a563e17e3eb; cna=bdCrHGAC/FkCAd3cZuiGIm7/; xlly_s=1; tfstk=cZPGBnwQTRk6a-1YAlG116ItUVIdaivZfSPTTZX7CLeZ9wFE7sXvLLJxtwmFVGJf.; isg=BPX1o4cH_cp0WRl2dV4tvYXqBHGvcqmEDfqucXcY4Wy7ThdAPsEfVMWPmBL4CcE8; l=fBjejtDgNBKCWiyZBO5CFurza77OzQAbz1PzaNbMiIEGa6CfTFM-bNC_8hG27dtjgT5DgeKrip0J_de67mULRAkDBeYCWQ0gUEpM8eM3N7AN.'
}
response = requests.get(url, headers=headers, params=params)
print(response.text)
