# OnlinePortScan

[![PythonVersion](https://img.shields.io/badge/Python-v3.5-blue?logo=python&style=flat-square)](https://www.python.org/downloads/)

支持代理的匿名在线端口扫描脚本

## 介绍

收集并使用网络上的API，实现简单匿名化的端口扫描，不一定能保证百分百的准确性。

## 使用

* 安装python，版本 >= `3.5`
* 安装依赖的库  `pip install -r requirements.txt`
* 克隆或下载本仓库代码
* 命令行使用（不能直接设置代理）
    ```powershell
    PS C:\Users\> python onlineportscan.py --h example.com --p 80 443 --s y  # 扫描主机example.com  端口80和443 保存记录文件默认位置 默认使用api-1
    ...
    PS C:\Users\> python onlineportscan.py --h example.com --pr 20 22 --s y --a 2  # 扫描主机example.com  端口范围20到22 保存记录文件默认位置 使用api-2
    ...
    PS C:\Users\> python onlineportscan.py --h 8.8.8.8 --pr 100 180 --t 15 --a 3  # 扫描主机8.8.8.8 端口范围100到180 不保存记录 设置最大工作线程为15 使用api-3
    ...
    PS C:\Users\> python onlineportscan.py -h # 获取帮助
    usage: onlineportscan.py [-h] [-port P [P ...]] [-portrange PR PR] -host H [-api {1,2,3}] [-detail {y,n,Y,N}] [-filepath F]
                            [-save {y,n,Y,N}] [-thread T]

    输入些运行参数，如若设置代理或其它，需在代码里修改配置运行

    optional arguments:
    -h, --help            show this help message and exit
    -port P [P ...], --p P [P ...]
                            扫描的端口，默认80，可多个，例如： --p 80 443
    -portrange PR PR, --pr PR PR
                            扫描的端口范围，两个参数，例如： --pr 20 22
    -host H, --h H        扫描的主机，例如：--h example.com
    -api {1,2,3}, --a {1,2,3}
                            在线扫描API选择，默认 1，目前有1，2，3，例如：--a 1
    -detail {y,n,Y,N}, --d {y,n,Y,N}
                            打印每个端口的执行结果，默认 n 不保存，y表示保存，不分大小写，例如：--d n
    -filepath F, --f F    记录保存路径，默认在该脚本目录下，名为port_scan_records.txt，例如：--f D:/port_scan_records.txt
    -save {y,n,Y,N}, --s {y,n,Y,N}
                            是否保存文件，默认 n 不保存，y表示保存，不分大小写，例如：--s y
    -thread T, --t T      选择最大工作线程数，例如：--t 10
    ```
* 导入使用（可设置代理）
    ```python
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
    ```
# 免责声明

本脚本仅提供交流和学习的机会。

# License

The GPL-3.0 License.