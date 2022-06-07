# coding=utf-8

"""
@Author       :  Ayouth
@Date         :  2022-06-07 GMT+0800
@LastEditTime :  2022-06-07 GMT+0800
@FilePath     :  req.py
@Description  :  Python 异步http请求测试
@Copyright (c) 2022 by Ayouth, All Rights Reserved. 
"""
import asyncio
import time
import aiohttp
import os


async def make_request(client: aiohttp.ClientSession, url: str, method: str) -> None:
    async with client.request(url=url, method=method) as resp:
        if resp.status != 200:
            print("status error:", resp.status)


async def reqs(url: str, method: str, count: int, limit: int) -> None:
    con = aiohttp.TCPConnector(limit=limit)
    async with aiohttp.ClientSession(connector=con, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept":     "*/*",
    }) as client:
        tasks = [asyncio.create_task(make_request(client, url, method))
                 for _ in range(count)]
        await asyncio.gather(*tasks)


def timer(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print("time spent:\t%.2fs" % (end-start))
    return wrapper


@timer
def run(url: str, method: str = "GET", count: int = 100, limit: int = 64) -> None:
    """
    @description: 执行函数
    @param {str} url 
    @param {str} method 
    @param {int} count 
    @param {int} limit 最大并发数
    @return {*}
    """
    if os.name == 'nt':
        # windows 需要设置
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(reqs(url, method, count, limit))
    print("url:\t%s\nmethod:\t%s\ncount:\t%s\nlimit:\t%s" %
          (url, method, count, limit))


if __name__ == '__main__':

    # 请求本地构建的服务器
    # run(
    #     url="http://127.0.0.1:8080/",
    #     method="GET",
    #     count=10000,
    #     limit=64  # 最大并发数
    # )

    # 请求远程服务器
    run(
        url="https://www.jb51.net/",
        method="GET",
        count=500,
        limit=64  # 最大并发数
    )
