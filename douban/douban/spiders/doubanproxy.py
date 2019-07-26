import re
import time

import requests
import datetime
from scrapy import signals
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError


# 全局变量-》代理地址
proxy_ip = ''
# 全局变量-》 代理池
proxy_array = []
# 全局变量-》失败代理地址
fail_proxy_ip = ''
# 接口地址
proxy_api = 'https://proxy.horocn.com/api/proxies?order_id=LYZF1630215813801599&format=text&line_separator=win&can_repeat=yes&num=1'
proxy_api_count = 'https://proxy.horocn.com/api/proxies?order_id=LYZF1630215813801599&format=text&line_separator=win&can_repeat=yes&num='
# 代理超时时间
proxy_expire_time = datetime.datetime.now() + datetime.timedelta(minutes=3)

proxy_array_size = 10

def getRandomIP():

    global proxy_array
    global proxy_array_size
    if len(proxy_array)*2 < proxy_array_size:
        fillProxyIP(proxy_array_size)
    ip = random.choice(proxy_array)
    return ip

def fillProxyIP(count):
    global proxy_api_count
    global proxy_array
    global proxy_array_size
    print("获取" + str(count) + "个IP")
    response = requests.get(proxy_api_count + str(count))

    if response.status_code == 200:
        ipTxt = response.text
        list = ipTxt.split("\r\n")
        fillIndex = 0
        for ipStr in list:
            if ipStr != '':
                if(len(ipStr) <= 25):
                    proxy_array.append(ipStr)
                    fillIndex = fillIndex + 1
        if fillIndex == 0:
            print(ipTxt)
            time.sleep(10)
            fillProxyIP(count)
        print(proxy_array)
    else :
        time.sleep(10)
        fillProxyIP(count)
    # print("IP池情况")
    # print(proxy_array)

def removeProxyIP(ip):
    global proxy_array
    # print(proxy_array)
    old_ip = ip.replace('\r', '')
    old_ip = old_ip.replace('\n','')
    old_ip = old_ip.replace('https://','')
    old_ip = old_ip.replace('http://','')
    # print("移除IP: {%s}"%(old_ip))
    if old_ip in proxy_array:
        proxy_array.remove(old_ip)