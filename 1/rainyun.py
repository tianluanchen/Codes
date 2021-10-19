import requests
import re
import time
from pathlib import Path

#    Author:        tianluanchen
#    date:          2021/10/3
#    description:   Automatically sign in to receive points on rainyun


class RainYun():
    def __init__(self, user, pwd,log_path="rainyun_log.csv"):
        self.user = user
        self.pwd = pwd
        self.log_path = log_path
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.0 Safari/537.36 Edg/96.0.1028.0",
            "origin": "https://www.rainyun.com",
        }
        self.session = requests.session()
        self.login_url = "https://www.rainyun.com/login"
        self.sign_url = "https://www.rainyun.com/app/usr/reward"
        self.logout_url = "https://www.rainyun.com/app/logout"

    def get_token(self):
        res = self.session.get(url=self.login_url, headers=self.headers)
        text = res.content.decode(res.apparent_encoding)
        # 正则提取
        # print(text)
        token = re.findall('data: {_token:"(.*?)", log_name:', text)[0]
        # print(token)
        self.token = token

    def login(self):
        self.get_token()
        data = {
            "_token": self.token,
            "log_name": self.user,
            "log_pass": self.pwd,
            "log_isremember": 0
        }
        res = self.session.post(
            url=self.login_url, headers=self.headers, data=data)
        text = res.content.decode(res.apparent_encoding)
        if text == "1":
            print('雨云：用户 ' + self.user + " 登录成功！")
        else:
            print('雨云：用户 ' + self.user + " 登录失败！")

    def sign_in(self):
        data = {
            "_token": self.token,
            "Action": "GetReward",
            "TaskName": "每日签到",
        }
        res = self.session.post(
            url=self.sign_url, headers=self.headers, data=data)
        text = res.text
        if text == "1":
            print('雨云：用户 ' + self.user + ' 成功签到并领取积分！')
            self.sign_status = 'success'
        else:
            print('雨云：用户 ' + self.user + ' 领取每日签到积分失败！')
            self.sign_status = 'failure'

    def logout(self):
        res = self.session.get(url=self.logout_url, headers=self.headers)
        print('雨云：用户 ' + self.user + ' 已退出登录！')

    def log(self):
        log_time = time.strftime("%Y/%m/%d %H:%M:%S")
        log_file = Path(self.log_path)
        if log_file.is_file():
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(log_time + ',' + self.user +
                        ',' + self.sign_status + '\n')
        else:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.write('date,user,status\n')
                f.write(log_time + ',' + self.user +
                        ',' + self.sign_status + '\n')
        print('雨云：用户 ' + self.user + ' 积分签到日志保存成功！')


if __name__ == '__main__':
    # 账户
    user = ""
    # 密码
    password = ""
    # log存储路径可自定义，也可不填写，默认为"rainyun_log.csv"，注意文件名应为.csv后缀
    # log_path = ""
    # demo = RainYun(user, password,log_path)
    # 初始化填写密码账户
    demo = RainYun(user, password)
    # 登录
    demo.login()
    # 签到
    demo.sign_in()
    # 退出登录
    demo.logout()
    # 日志保存
    demo.log()
