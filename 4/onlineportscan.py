# coding=utf-8

"""
@Author       :  Ayouth
@Date         :  2022-02-20 GMT+0800
@LastEditTime :  2022-07-05 GMT+0800
@FilePath     :  onlineportscan.py
@Description  :  端口在线扫描
@Copyright (c) 2022 by Ayouth, All Rights Reserved. 
"""

import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from fake_useragent import UserAgent
import json
import time
import re
from websocket import create_connection
import os
from faker import Faker


class PortScaner():
    '''
        支持代理的匿名在线端口扫描类

        可自定义属性或参数:
            host:           主机名
            max_worker:     最大数量工作线程
            porxies:        api1和api2的代理
            ws_proxy:       api3的websocket的代理
            file_path:      记录保存位置，包含文件名 默认该脚本同属目录 文件名为port_scan_records.txt
            ports:          端口列表，0到65535 多个
            port_start:     端口范围 起始端口 同时设置 端口范围优先级大于端口列表
            port_end:       端口范围 结束端口 若不设置则只扫描一个port_start
            detail:         True或False 默认True  打印每一个端口扫描任务结果
            save:           默认True 保存每次扫描的结果

        # 示例用法
        >>> host = "google.com"
        >>> proxies = {
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080'
            }
        >>> ws_proxy = {
                'host': '127.0.0.1',
                'port': 8080
            }
        # 默认保存记录文件至脚本同属目录
        >>> case = PortScaner(host, proxies=proxies, ws_proxy=ws_proxy)
        >>> case.scan(port_start=70, port_end=80, api=1)
        # 设置不保存结果至文件且不打印详情
        >>> case.scan(ports=[440, 443], api=3, detail=False, _save_record=False)
        # 自定义记录文件路径 和最大工作线程
        >>> my_file_path = 'D:/test.txt'
        >>> case.update(host, max_worker=14, proxies=proxies,
                    ws_proxy=ws_proxy, file_path=my_file_path)
        >>> case.scan(ports=[440, 443], api=2)
    '''

    def __init__(self, host: str, max_worker: int = None, proxies: dict = {
            'http': None, 'https': None}, ws_proxy: dict = None, file_path: str = None) -> None:
        '''
        初始化host max_worker proxies ws_proxy file_path等属性
        '''
        self.host = host
        self._ua = UserAgent()
        self.max_worker = max_worker
        self.proxies = proxies
        self.file_path = file_path
        self._first_api_token = None
        self.ws_proxy = ws_proxy
        self._faker = Faker()
        if file_path is None:
            self.file_path = os.path.dirname(
                os.path.realpath(__file__))+'\port_scan_records.txt'
        else:
            self.file_path = file_path

    def update(self, host: str, max_worker: int = None, proxies: dict = {
            'http': None, 'https': None}, ws_proxy: dict = None, file_path: str = None):
        '''
            更新host max_worker proxies ws_proxy file_path等属性
        '''
        self.host = host
        self.max_worker = max_worker
        self.proxies = proxies
        self.ws_proxy = ws_proxy
        if file_path is not None:
            self.file_path = file_path

    def scan(self, ports: list = None, port_start: int = -1, port_end: int = -1, api: int = 1, detail: bool = True, save: bool = True) -> None:
        '''
            扫描 设置ports port_start port_end api detail save等属性或参数
        '''
        self.detail = detail
        self.ports = ports
        if port_end == -1 or port_end < port_start:
            port_end = port_start
        self.port_start = port_start
        self.port_end = port_end
        if self.ports is None and self.port_start < 0:
            exit('端口起始不能小于0！')
        elif self.port_start >= 0:
            self.ports = [port for port in range(
                self.port_start, self.port_end+1)]
        for i in range(len(self.ports)):
            if self.ports[i] < 0 or self.ports[i] > 65535:
                del self.ports[i]
        self.open_ports = []
        self.error_log = []
        self.start = time.time()
        print()
        if api == 1:
            self._first_api()
        elif api == 2:
            self._second_api()
        else:
            self._third_api()
        self.end = time.time()
        self.duration = round(self.end-self.start, 2)
        self._print_result()
        if save:
            self._save_record()

    def _first_api(self):
        '''
            api-1 proxie属性对此有效
        '''
        if self._first_api_token is None:
            self._get_first_api_token()
        self.current_excute_api = 'first_api'
        with ThreadPoolExecutor(max_workers=self.max_worker) as pool:
            task_list = []
            for port in self.ports:
                task_list.append(pool.submit(self._first_api_request, port))
            wait(task_list, return_when=ALL_COMPLETED)

    def _first_api_request(self, port: int):
        '''
            api-1 发送请求
        '''
        url = 'https://tool.chinaz.com/iframe.ashx?t=port&callback=jQuery11130457' + \
            str(int(time.time()))+'_'+str(int(time.time()))
        random_ipv4 = self._faker.ipv4()
        headers = {
            "User-Agent": self._ua.random,
            'Host': 'tool.chinaz.com',
            'Origin': 'https://tool.chinaz.com',
            'Referer': 'https://tool.chinaz.com/port',
            "Via": random_ipv4,
            'X-Forwarded-For': random_ipv4,
            'Client-Ip': random_ipv4
        }
        data = {
            'port': port,
            'host': self.host,
            'encode': self._first_api_token
        }
        try:
            res = requests.post(url=url, headers=headers,
                                data=data, verify=False, proxies=self.proxies)
            pattern = r'{status:(\d),msg'
            status = 'Closed'
            if re.search(pattern, res.text).group(1) == '1':
                self.open_ports.append(port)
                status = 'Open'
            if self.detail:
                print('first_api > port: %s    status: %s' % (port, status))
        except Exception as e:
            with open(r'C:\Users\30869\Desktop\网络安全\error.txt', 'w') as f:
                f.write(res.text)
            # 访问异常的错误编号和详细信息
            if self.detail:
                print('first_api > port:', port, '   error:', repr(e))
            self.error_log.append(
                {'api': 'first_api', 'port': port, 'error': repr(e)})

    def _get_first_api_token(self):
        '''
            api-1 需要token
        '''
        random_ipv4 = self._faker.ipv4()
        headers = {
            'Host': 'tool.chinaz.com',
            'Origin': 'https://tool.chinaz.com',
            'Referer': 'https://tool.chinaz.com/port',
            'X-Forwarded-For': random_ipv4,
            'Client-Ip': random_ipv4,
            'Via': random_ipv4,
            'User-Agent': self._ua.random
        }
        url = 'https://tool.chinaz.com/port'
        data = data = {
            'port': 80,
            'host': 'www.baidu.com',
        }
        res = requests.post(url, data=data, headers=headers, verify=False, proxies={
                            'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'})
        pattern = r'<input type="hidden" id="encode" value="(.+?)" />'
        result = re.search(pattern, res.content.decode('utf-8'))
        if result:
            self._first_api_token = result.group(1)
        else:
            self._first_api_token = None
            exit('first_api 无法获取token，所以强制退出')

    def _second_api(self) -> None:
        '''
            api-2 proxies对此有效
        '''
        self.current_excute_api = 'second_api'
        with ThreadPoolExecutor(max_workers=self.max_worker) as pool:
            task_list = []
            for port in self.ports:
                task_list.append(pool.submit(self._second_api_request, port))
            wait(task_list, return_when=ALL_COMPLETED)

    def _second_api_request(self, port: int) -> None:
        '''
            api-2 请求
        '''
        url = "http://duankou.wlphp.com/api.php"
        random_ipv4 = self._faker.ipv4()
        headers = {
            "User-Agent": self._ua.random,
            "Host": "duankou.wlphp.com",
            "Via": random_ipv4,
            'X-Forwarded-For': random_ipv4,
            'Client-Ip': random_ipv4
        }
        data = {
            "i": self.host,
            "p": port
        }
        try:
            res = requests.post(url=url, headers=headers,
                                data=data, verify=False, proxies=self.proxies)
            dic = res.json()
            status = 'Closed'
            if dic['msg']['status'] == 'Openning':
                self.open_ports.append(port)
                status = 'Open'
            if self.detail:
                print('second_api > port: %s    status: %s' % (port, status))
        except Exception as e:
            # 访问异常的错误编号和详细信息
            if self.detail:
                print('second_api > port:', port, '   error:', repr(e))
            self.error_log.append(
                {'api': 'second_api', 'port': port, 'error': repr(e)})

    def _third_api_request(self, port):
        '''
            api-3 请求
        '''
        random_ipv4 = self._faker.ipv4()
        headers = {
            "User-Agent": self._ua.random,
            "Host": "d_uankou.wlphp.com",
            "Via": random_ipv4,
            'X-Forwarded-For': random_ipv4,
            'Client-Ip': random_ipv4,
            'Host': 'coolaf.com:9010',
            'Origin': 'http://coolaf.com',
            'Cookie': 'iris.lang_uage=zh; urladd='
        }
        uri = "ws://coolaf.com:9010/tool/ajaxport"
        try:
            if self.ws_proxy is None:
                ws = create_connection(uri, headers=headers)
            else:
                ws = create_connection(
                    uri, headers=headers, http_proxy_host=self.ws_proxy['host'], http_proxy_port=self.ws_proxy['port'])
            ws.send('{"ip":"%s","port":"%d"}' % (self.host, port))
            result = ws.recv()
            dic = json.loads(result)
            status = 'Closed'
            if dic['Status'] == '1':
                self.open_ports.append(port)
                status = 'Open'
            if self.detail:
                print("third_api > port:%d    status:%s" % (port, status))
        except Exception as e:
            if self.detail:
                print('third_api > port:', port, '   error:', repr(e))
            self.error_log.append(
                {'api': 'third_api', 'port': port, 'error': repr(e)})
        finally:
            ws.close()

    def _third_api(self) -> None:
        '''
            api-3 ws_proxy对此有效
        '''
        self.current_excute_api = 'third_api'
        with ThreadPoolExecutor(max_workers=self.max_worker) as pool:
            task_list = []
            for port in self.ports:
                task_list.append(pool.submit(self._third_api_request, port))
            wait(task_list, return_when=ALL_COMPLETED)

    def _print_result(self) -> None:
        '''
            打印扫描结果
        '''
        ports_string = ','.join([str(port) for port in self.open_ports])
        if ports_string == '':
            ports_string = '暂无'
        print()
        self.record_string = '时间： %s --- %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            self.start)), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end)))
        self.record_string += '\n'
        if self.port_start == -1:
            port_range = ','.join([str(port) for port in self.ports])
        else:
            port_range = '%d - %d' % (self.port_start, self.port_end)
        self.record_string += '主机： %s \n指定端口： %s \n已开放端口数量： %d \n已开放端口： %s' % (
            self.host, port_range, len(self.open_ports), ports_string)
        self.record_string += '\n'
        error_ports = []
        self.record_string += '任务出错的端口：'
        for error in self.error_log:
            error_ports.append(error['port'])
        if len(error_ports) <= 0:
            self.record_string += '暂无'
        else:
            self.record_string += ' , '.join([str(port)
                                             for port in error_ports])
        self.record_string += '\n本次任务由 %s 执行，一共花费了约 %.2f s\n' % (
            self.current_excute_api, self.duration)
        for error in self.error_log:
            self.record_string += 'API: %s    端口：%d    错误详情：%s\n' % (
                error['api'], error['port'], error['error'])
        print(self.record_string)

    def _save_record(self):
        '''
            存储记录
        '''
        try:
            with open(self.file_path, 'a+', encoding='utf-8') as f:
                f.writelines([self.record_string, '记录保存时间：', time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()), '\n\n'])
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  '\n文件路径', '"'+self.file_path+'"', '-', '记录保存成功')
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  '\n文件路径', '"'+self.file_path+'"', '-', '保存出错', '-', repr(e))
        print()


# 通过在线端口扫描api，隐藏自身ip
if __name__ == "__main__":
    def sys_args_excute():
        """
            命令行参数执行
        """
        parser = argparse.ArgumentParser(
            description='输入些运行参数，如若设置代理或其它，需在代码里修改配置运行')
        parser.add_argument('-port', '--p', type=int, nargs='+', default=[80],
                            help='扫描的端口，默认80，可多个，例如： --p 80 443')
        parser.add_argument('-portrange', '--pr', type=int, nargs=2, default=[-1, -1],
                            help='扫描的端口范围，两个参数，例如： --pr 20 22')
        parser.add_argument('-host', '--h', type=str, required=True,
                            help='扫描的主机，例如：--h example.com')
        parser.add_argument('-api', '--a', type=int, default=1, choices=[1, 2, 3],
                            help='在线扫描API选择，默认 1，目前有1，2，3，例如：--a 1')
        parser.add_argument('-detail', '--d', type=str, default='y', choices=['y', 'n', 'Y', 'N'],
                            help='打印每个端口的执行结果，默认 n 不保存，y表示保存，不分大小写，例如：--d n')
        parser.add_argument('-filepath', '--f', type=str, default=None,
                            help='记录保存路径，默认在该脚本目录下，名为port_scan_records.txt，例如：--f  D:/port_scan_records.txt')
        parser.add_argument('-save', '--s', type=str, default='n', choices=['y', 'n', 'Y', 'N'],
                            help='是否保存文件，默认 n 不保存，y表示保存，不分大小写，例如：--s y')
        parser.add_argument('-thread', '--t', type=int,
                            help='选择最大工作线程数，例如：--t 10')
        args = parser.parse_args()
        case = PortScaner(host=args.h, max_worker=args.t, file_path=args.f)
        case.scan(ports=list(set(args.p)), port_start=args.pr[0], port_end=args.pr[1], detail=True if args.d.lower() == 'y' else False,
                  save=False if args.s.lower() == 'n' else True, api=args.a)
        exit()
    import warnings
    warnings.filterwarnings('ignore')
    sys_args_excute()
