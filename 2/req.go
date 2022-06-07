/*
 * @Author       :  Ayouth
 * @Date         :  2022-06-07 GMT+0800
 * @LastEditTime :  2022-06-07 GMT+0800
 * @FilePath     :  req.go
 * @Description  :	GO Http异步请求测试
 * Copyright (c) 2022 by Ayouth, All Rights Reserved.
 */
package main

import (
	"flag"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"
)

func timer(fn func()) {
	start := time.Now()
	fn()
	dur := time.Since(start)
	fmt.Printf("time spent:\t%.2fs", dur.Seconds())
}

func req(client http.Client, url, method string) {
	req, err := http.NewRequest(method, url, nil)
	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Set(
		"User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
	)
	req.Header.Set(
		"Accept", "*/*",
	)
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	} else if resp.Status != "200 OK" {
		fmt.Println("Status Error:", resp.Status)
	}
}

func run(url, method string, count int, limit int) {
	method = strings.ToUpper(method)
	client := http.Client{}
	wg := sync.WaitGroup{}
	ch := make(chan struct{}, limit)
	for i := 0; i < count; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			ch <- struct{}{}
			req(client, url, method)
			<-ch
		}()
	}
	wg.Wait()
	fmt.Printf("url:\t%s\nmethod:\t%s\ncount:\t%d\nlimit:\t%d\n", url, method, count, limit)
}

func main() {

	var url string
	var method string
	var count int
	var limit int
	flag.StringVar(&url, "u", "http://127.0.0.1:8080/", "目标URL端口，默认http://127.0.0.1:8080/")
	flag.StringVar(&method, "m", "GET", "请求格式，默认GET")
	flag.IntVar(&count, "c", 500, "请求数量，默认500")
	flag.IntVar(&limit, "l", 64, "最大并发数，默认64")
	flag.Parse()

	timer(func() {
		run(
			url,
			method,
			count, // 请求数量
			limit, // 最大并发数
		)
	})
	// 请求本地构建的服务器
	// timer(func() {
	// 	run(
	// 		"http://127.0.0.1:8080/",
	// 		"GET",
	// 		10000, // 请求数量
	// 		64,    // 最大并发数
	// 	)
	// })

	// 请求远程服务器
	// timer(func() {
	// 	run(
	// 		"https://www.jb51.net/",
	// 		"GET",
	// 		500, // 请求数量
	// 		64,  // 最大并发数
	// 	)
	// })

}
