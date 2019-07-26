'''
    头条热点爬虫 100条
    https://www.toutiao.com/ch/news_hot/

'''

import scrapy
import base64



class TouTiaoHotSpider(scrapy.Spider):
    name = 'tthotspider'

    def __init__(self):
        self.start_urls = []

    def parse(self, response):
        print("")