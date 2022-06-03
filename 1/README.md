雨云积分签到 
=======

[![PythonVersion](https://img.shields.io/badge/Python-v3.5-blue?logo=python&style=flat-square)](https://www.python.org/downloads/) [![PHPVersion](https://img.shields.io/badge/PHP-v7.4-orange?logo=php&style=flat-square)](https://www.php.net/downloads)

## 介绍

实现[雨云](https://www.rainyun.com)平台自动签到领取积分，可扩展PHP程序进行日志审阅。

## 使用

* 环境配置

    安装Python3.5或以上版本，安装Requests库。
    若使用PHP程序，则安装PHP7.4或以上版本。

* Python签到脚本信息配置

    ```python
    #rainyun.py 120行左右
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
    ```

* 运行测试

    ```bash
    python rainyun.py
    # 查看输出判断是否成功 
    ```

* 部署定时任务实现每日自动签到

    上网搜索Windows或linux相关定时任务教程。宝塔用户可部署在宝塔计划任务中。
    
* 拓展PHP程序审阅日志
    
    将rainyun.php放在自己的环境下即可，注意rainyun.py和该php中填写的日志文件路径必须一致

    ```php
    //rainyun.php 15行左右
    //自定义网页标题和大标题
    $title = "雨云签到日志";
    //文件路径，推荐绝对路径
    $file = "./rainyun-signin-log.csv";
    //设置审阅令牌
    $token = "123";
    ```

    部署后Web页面演示

    [![日志管理页](https://s3.bmp.ovh/imgs/2022/06/03/722ef58dae4e061c.gif)](https://s3.bmp.ovh/imgs/2022/06/03/722ef58dae4e061c.gif)

