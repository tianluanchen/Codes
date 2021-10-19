import requests
import json
import re
from setting import POST_URL


# 获取下载直链
def get_directurl(offical_url, pwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }
    headers['referer'] = offical_url
    domain = re.findall('https://(.+?)/', offical_url)[0]
    post_url = 'https://' + domain + POST_URL
    data = {
        "action": "downprocess",
        "sign": "",
        "p": pwd,
    }
    res = requests.get(url=offical_url, headers=headers)
    sign = re.findall('action=downprocess&sign=(.+?)&p=', res.text)[0]
    data['sign'] = sign
    res = requests.post(url=post_url, headers=headers, data=data)
    Json = json.loads(res.content.decode(res.apparent_encoding))
    transfer_url = Json['dom'] + '/file/' + Json['url']
    # print(Json['inf'])
    res = requests.get(url=transfer_url, headers=headers, allow_redirects=False)
    download_url = res.headers.get('location')
    # print(res.status_code)
    # print(download_url)
    return download_url


if __name__ == '__main__':
    get_directurl('https://wws.lanzoui.com/iaVesvilm1i', '301d')
