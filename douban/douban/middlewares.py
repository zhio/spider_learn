# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import requests
import datetime
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


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

proxy_array_size = 20

def getRandomIP():

    global proxy_array
    global proxy_array_size
    if len(proxy_array)*2 < proxy_array_size:
        fillProxyIP(proxy_array_size)
    ip = random.choice(proxy_array)
    # print("使用IP:{%s}"%(ip))
    return ip

def fillProxyIP(count):
    global proxy_api_count
    global proxy_array
    global proxy_array_size
    print("获取" + str(count) + "个IP")
    response = requests.get(proxy_api_count + str(count))
    # print(response.text)

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
        getProxyIPError(response.text)
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



def getProxyIPError(str):
    print("【错误】代理获取失败 {%s}"%(str))

class FlamaoyanspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 代理中间件
class FlaProxyMiddleware(object):
    global proxy_ip
    global fail_proxy_ip
    global proxy_api
    global proxy_expire_time
    global proxy_array_size
    def __init__(self):
        #reGetProxyIP()
        fillProxyIP(proxy_array_size)

        # global proxy_ip
        # proxy_ip = "125.123.126.162:26158"

    # 发送请求
    def process_request(self,request,spider):
        # if 'X-Requested-With' in request.headers:
        #     print("尝试获取ajax请求，保持Ip不变")
        #     if request.meta.__contains__('retry_times'):
        #         retry_times = int(request.meta['retry_times'])
        #         if retry_times > 2:
        #             url  = request.headers['Referer'].decode('utf-8')
        #             headers = {'User-Agent':request.headers['User-Agent']}
        #             return  request.replace(url = url,headers = headers,callback = spider.parse)
        # else:
        global fail_proxy_ip
        # print("request.meta = %s" %(request.meta))
        isReset = False
        if request.meta.__contains__('retry_times'):
            retry_times = int(request.meta['retry_times'])
            if retry_times > 2:
                #fail_proxy_ip = request.meta['proxy']
                #reGetProxyIP()
                if 'proxy' in request.meta:
                    removeProxyIP(request.meta['proxy'])
                    isReset = True
            # if proxy_ip:
            #     uri = 'https://{proxy}'.format(proxy=proxy_ip)
            #     request.meta['proxy'] = uri
        uri = 'https://{proxy}'.format(proxy = getRandomIP())
        request.meta['proxy'] = uri

    #接收请求
    @staticmethod
    def process_response(request, response, spider):
        global fail_proxy_ip
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            #fail_proxy_ip = request.meta['proxy']
            print("【警告】状态码异常：{%s}  请求地址{%s}"%(format(response.status),request.url))
            #reGetProxyIP()
            removeProxyIP(request.meta['proxy'])
            return request
        if response is None:
            #fail_proxy_ip = request.meta['proxy']
            print("【警告】返回空类型")
            #reGetProxyIP()
            removeProxyIP(request.meta['proxy'])
            return request
        if len(response.text) == 0:
            #fail_proxy_ip = request.meta['proxy']
            print("【警告】返回空字符串:Status-->{} Response-->{}".format(response.status, response.text))
            #reGetProxyIP()
            removeProxyIP(request.meta['proxy'])
            return request
        return response

# UserAgent中间件
class MyUserAgentMiddleware(UserAgentMiddleware):
    global proxy_ip
    global fail_proxy_ip
    global proxy_api
    global proxy_expire_time
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        if 'X-Requested-With' in request.headers:
            print("尝试获取ajax请求，保持User-Agent不变")
        else:
            agent = random.choice(self.user_agent)
            request.headers['User-Agent'] = agent
            request.headers['Referer'] = 'piaofang.maoyan.com'
import logging
class ModifyStartRequest(object):

    def process_start_requests(self, start_requests, spider):
        logging.debug("#### 2222222 start_requests %s , spider %s ####" % (start_requests, spider))
        last_request = []
        for one_request in start_requests:
            logging.debug("#### one_request %s , spider %s ####" % (one_request, spider))
            last_request.append(one_request)
        logging.debug("#### last_request %s ####" % last_request)
        return last_request


class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

