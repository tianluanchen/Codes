/*
 * @Author       :  Ayouth
 * @Date         :  2022-06-06 GMT+0800
 * @LastEditTime :  2022-06-07 GMT+0800
 * @FilePath     :  server.go
 * @Description  :	服务器程序
 * Copyright (c) 2022 by Ayouth, All Rights Reserved.
 */
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"
)

func main() {
	var port int
	var host string
	var ms int
	flag.IntVar(&port, "p", 8080, "服务器端口，默认8080")
	flag.StringVar(&host, "h", "127.0.0.1", "主机名，默认127.0.0.1")
	flag.IntVar(&ms, "s", 400, "模拟正常网站响应的延迟，单位毫秒，默认400")
	flag.Parse()
	http.HandleFunc("/", func(rw http.ResponseWriter, req *http.Request) {
		// 模拟现实网站等待0.4s
		time.Sleep(time.Millisecond * 400)
		log.Println(req.Method, req.URL.Path, req.RemoteAddr)
		rw.Header().Set("Content-Type", "text/html;charset=utf8")
		fmt.Fprintf(rw, "Success")
	})
	addr := fmt.Sprint(host, ":", port)
	fmt.Printf("url:\thttp://%s\ndelay:\t%dms\n", addr, ms)
	err := http.ListenAndServe(addr, nil)
	if err != nil {
		panic(err)
	}
}
