import requests
import json
import re
from setting import POST_URL

# 有密碼
def with_pwd(share_url, pwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }
    headers['referer'] = share_url
    domain = re.findall('https://(.+?)/', share_url)[0]
    post_url = 'https://' + domain + POST_URL
    data = {
        "action": "downprocess",
        "sign": "",
        "p": pwd,
    }
    res = requests.get(url=share_url, headers=headers)
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

# 无密码
def without_pwd(share_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }
    # 当前分享链接的域名
    domain = re.findall('https://(.+?)/', share_url)[0]
    res = requests.get(url=share_url, headers=headers)
    text = res.content.decode(res.apparent_encoding)
    # 获取iframe url
    if share_url[-1] == '/':
        iframe_url = share_url + re.findall('src="/(fn.+?)"', text)[0]
    else:
        iframe_url = share_url + re.findall('src="(/fn.+?)"', text)[0]
    # print(iframe_url)
    # 设置iframe的referer
    headers['referer'] = share_url
    res = requests.get(url=iframe_url, headers=headers)
    text = res.content.decode(res.apparent_encoding)
    with open('res.html','wb')as f:
        f.write(res.content)
    ajaxdata = re.findall("ajaxdata = '(.+?)'",text)[0]
    pattern="var ajaxdata = '.+?';\n		var (.+?) = '(.+?)'"
    sign = re.findall(pattern,text)[0]
    wsk = re.findall("'websignkey':'(.+?)'",text)[0]
    data = {
        "action": "downprocess",
        "signs": ajaxdata,
        "sign": sign,
        "ves": "1",
        "websign": "",
        "websignkey": wsk,
    }
    # 发送数据获取最终url
    post_url = 'https://' + domain + POST_URL
    res = requests.post(url=post_url, headers=headers, data=data)
    Json = json.loads(res.content.decode(res.apparent_encoding))
    # print(Json)
    transfer_url = Json['dom'] + '/file/' + Json['url']
    # print(Json['inf'])
    # print(transfer_url)
    res = requests.get(url=transfer_url, headers=headers, allow_redirects=False)
    download_url = res.headers.get('location')
    # print(res.status_code)
    # print(download_url)
    return download_url

# 获取下载直链
def get_directurl(share_url, pwd=None):
    if pwd:
        return with_pwd(share_url, pwd)
    else:
        return without_pwd(share_url)


if __name__ == '__main__':
    url = get_directurl('https://wws.lanzoui.com/iaVesvilm1i', '301d')
    print(url)
    # without_pwd('https://lanzoui.com/FkkdyRjh')
    pass
