雨云积分签到 
=======

<a href="https://github.com/tianluanchen/scripts/">![author](https://img.shields.io/badge/author-ayouth-green)</a>

## 介绍

本脚本面向使用[雨云](https://www.rainyun.com)云服务的用户，用来实现雨云平台自动签到领取积分，可扩展web进行日志查看和管理。

## 使用

* 下载 
    
    [点击下载该文件夹压缩包](http://33h.co/9gktj)

* 环境配置

    安装python3和requests库。

* Python脚本配置

    ```python
        #rainyun.py
        #文件配置，可在八九十行左右找到以下代码进行修改
        # 填写自己账户
        user = ""
        # 密码
        password = ""
        # log存储路径可自定义，也可不填写，默认为"rainyun_log.csv"，注意文件名应为.csv后缀
        # 例如linux下写绝对路径 /root/rainyun_log.csv
        log_path = "/root/rainyun_log.csv"
        demo = RainYun(user, password, log_path)
    ```
* 运行测试

    ```bash
    python rainyun.py
    # 查看输出判断是否成功 
    ```
* 自动签到部署

    为rainyun.py设置定时任务即可。例如可部署在宝塔计划任务中。
* 通过web访问对日志管理
    > 自行部署web服务器，并配置php环境，php版本 >= 5.6

    ```php
    //在rainyun_log.php中修改配置
    //自定义网页标题
    $html_title = "log";
    //文件路径，推荐绝对路径
    //例
    $file_path = "log.csv";
    //设置验证码
    $token = "1234";
    ```

    > 以本地为例,服务器运行后，按上例可通过访问 http://127.0.0.1/rainyun_log.php?token=1234 来管理


