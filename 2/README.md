GO,Python 异步HTTP请求测试
=======

[![PythonVersion](https://img.shields.io/badge/Python-v3.8.5-blue?logo=python&style=flat-square)](https://www.python.org/downloads/) [![GoVersion](https://img.shields.io/badge/Go-v1.17.2-blue?logo=go&style=flat-square)](https://go.dev/dl/)

## 介绍

测试Go和Python异步HTTP请求的性能，或是利用这些程序去对网站进行请求测试。Go使用标准库，Python使用第三方库`aiohttp`，分别对通过Go搭建简单的本地服务器和对真实网站进行请求测试，其中本地服务器设置了延时响应以模拟真实网站。

## 测试

Windows用户可以运行bin目录下的exe，如在命令行敲入`./server.win.exe -h`查看提示，也可以直接在req.go、req.py、server.go中修改代码进行运行，其中server.go用来搭建本地服务器，其余则都是http请求的代码。

## 结果（仅供参考）

针对本地服务器，响应延时400ms，两者都设置最大并发请求数为64，进行10000次请求，Python比Go慢了1秒左右，总体上来说大差不差，由于Go的协程是多核多线程的，Python只有单线程，这样的一个结果对于Python来说还是不错的表现，也表明了对于异步HTTP请求来说，两者在性能方面都能满足大多数需求。

在针对实际网站，如脚本之家时，网络环境等影响因素过多，导致测试结果变化大，在这方面已经不是编程语言的问题了。此外，很多网站都会有反爬虫等措施，开发者需要控制诸如请求并发数，请求间隔等，否则很容易出现IP被封，网络IO中断，数据错误等问题。

总的来说，更对推荐开发者使用Python进行爬虫工作，原因如下：

1. 在网络请求上和Go性能差距不大，都能实现高效的异步爬虫
2. 一般爬虫的目的还是以获取数据为准，由于Go强类型的语言，对数据类型要求严格，而我们爬虫获取的数据往往具有较大的不确定性和复杂性，Python作为弱类型的脚本语言，恰好适合解决此类问题。另外Python在爬虫方面的生态比Go更加完善，知名且稳定的第三方库众多，上手快，并且对爬虫遇到的问题都有成熟的解决方案。

当然如果你擅长Go语言，大可使用Go，Go的生态也在近些年来逐渐完善，关于爬虫也有一个火热的[colly](https://github.com/gocolly/colly)第三方库。至于不太擅长Go的开发者，Python无疑是一个不错的选择。

本地服务器测试结果
```powershell
$ go run req.go
url:    http://127.0.0.1:8080/
method: GET
count:  10000
limit:  64
time spent:     65.08s
$ python req.py
url:    http://127.0.0.1:8080/
method: GET
count:  10000
limit:  64
time spent:     66.37s
$ go run req.go
url:    http://127.0.0.1:8080/
method: POST
count:  10000
limit:  64
time spent:     64.65s
$ python req.py
url:    http://127.0.0.1:8080/
method: POST
count:  10000
limit:  64
time spent:     65.98s
```

远程服务器脚本之家测试结果
```powershell
$ python req.py
url:    https://www.jb51.net/
method: GET
count:  500
limit:  64
time spent:     8.83s
$ go run req.go
url:    https://www.jb51.net/
method: GET
count:  500
limit:  64
time spent:     6.79s
$ python req.py
url:    https://www.jb51.net/
method: GET
count:  500
limit:  64
time spent:     6.08s
$ go run req.go
url:    https://www.jb51.net/
method: GET
count:  500
limit:  64
time spent:     5.04s
```