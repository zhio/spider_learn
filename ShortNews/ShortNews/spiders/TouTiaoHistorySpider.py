'''
    头条热点爬虫 100条
    https://www.toutiao.com/ch/news_history/

'''

import scrapy
import base64


class TouTiaoHistorySpider(scrapy.Spider):
    name = 'tthistoryspider'

    def __init__(self):
        self.start_urls = []

    def parse(self, response):
        print("")