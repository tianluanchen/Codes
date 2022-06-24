# coding=utf-8

"""
@Author       :  Ayouth
@Date         :  2021-10-03 GMT+0800
@LastEditTime :  2022-06-24 GMT+0800
@FilePath     :  rainyun.py
@Description  :  雨云积分签到脚本
@Copyright (c) 2022 by Ayouth, All Rights Reserved. 
"""
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging
import json


class RainYun():

    def __init__(self, user: str, pwd: str) -> None:
        """
        @description: 初始化
        @param {*} self
        @param {str} user 用户名
        @param {str} pwd  密码
        @param {str} log_file 日志文件路径
        @return {*}
        """
        # 认证信息
        self.user = user
        self.pwd = pwd
        self.json_data = json.dumps({
            "field": self.user,
            "password": self.pwd
        })
        # 日志输出
        self.logger = logging.getLogger(self.user)
        formatter = logging.Formatter(datefmt='%Y/%m/%d %H:%M:%S',
                                      fmt="%(asctime)s 雨云 %(levelname)s: 用户<%(name)s> %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        # 签到结果初始化
        self.signin_result = False
        # 请求设置
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "Origin": "https://api.rainyun.com",
            "Referer": "https://api.rainyun.com"
        })
        self.login_url = "https://api.v2.rainyun.com/user/login"
        self.signin_url = "https://api.v2.rainyun.com/user/reward/tasks"
        self.logout_url = "https://api.v2.rainyun.com/user/logout"

    def login(self) -> None:
        """
        @description: 登录
        @param {*} self
        @return {*}
        """
        res = self.session.post(
            url=self.login_url, headers={"Content-Type": "application/json"}, data=self.json_data)
        if res.text.find("200") > -1:
            self.logger.info("登录成功")
            self.session.headers.update({
                "X-CSRF-Token": res.cookies.get("X-CSRF-Token", "")
            })
        else:
            self.logger.error(f"登录失败，响应信息：{res.text}")

    def signin(self) -> None:
        """
        @description: 签到
        @param {*} self
        @return {*}
        """
        res = self.session.post(url=self.signin_url, headers={"Content-Type": "application/json"}, data=json.dumps({
            "task_name": "每日签到",
            "verifyCode": ""
        }))
        if res.text.find("200") > -1:
            self.logger.info("成功签到并领取积分")
            self.signin_result = True
        else:
            self.logger.error(f"签到失败，响应信息：{res.text}")
            self.signin_result = False

    def logout(self) -> None:
        res = self.session.post(url=self.logout_url)
        if res.text.find("200") > -1:
            self.logger.info('已退出登录')
        else:
            self.logger.warning(f"退出登录时出了些问题，响应信息：{res.text}")

    def log(self, log_file: str) -> None:
        """
        @description: 存储本次签到结果的日志
        @param {*} self
        @param {str} log_file 日志文件，推荐绝对路径
        @return {*}
        """
        # 北京时间
        now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
            timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")
        file = Path(log_file)
        if file.is_file():
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write('{},{},{}\n'.format(
                    now, self.user, self.signin_result))
            self.logger.info('日志追加成功')
        else:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.writelines(['date,user,result\n', '{},{},{}\n'.format(
                    now, self.user, self.signin_result)])
            self.logger.info('新建日志成功')


if __name__ == '__main__':
    user = "example"  # 账户
    password = "123"  # 密码
    case = RainYun(user, password)  # 实例
    case.login()  # 登录
    case.signin()  # 签到
    case.logout()  # 登出
    # 保存日志则打开注释 推荐文件绝对路径
    # file = "./rainyun-signin-log.csv"
    # case.log(file)  # 保存日志
