#!/usr/bin/env python
# coding=utf-8

"""
@Author       :  Ayouth
@Date         :  2022-02-20 GMT+0800
@LastEditTime :  2022-03-13 GMT+0800
@FilePath     :  test.py
@Description  :  测试
@Copyright (c) 2022 by Ayouth, All Rights Reserved. 
"""
from onlineportscan import PortScaner
# 代理
# proxies = {
#     'http': 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }
# ws_proxy = {
#     'host': '127.0.0.1',
#     'port': 8080
# }
# case = PortScaner(host='python.org', proxies=proxies, ws_proxy=ws_proxy)
case = PortScaner(host='python.org')
case.scan([80, 443], api=1, save=False)
case.scan([80, 443], api=2, save=False)
case.scan([80, 443], api=3, save=False)
