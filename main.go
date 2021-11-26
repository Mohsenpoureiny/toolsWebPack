package main

import (
  "io/ioutil"
  "log"
  "net/http"
)

func main(){
  resp , err := http.Get("http://172.17.0.1:5000")
  if err != nil {
    log.Fatalln(err)
  }

  body , err := ioutil.ReadAll(resp.Body)
  if err !=nil{
    log.Fatalln(err)
  }
  sb := string(body)
  log.Printf(sb)
}

