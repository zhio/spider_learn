'''
    头条搞笑爬虫 100条
    https://www.toutiao.com/ch/funny/

'''

import scrapy
import base64



class TouTiaoFunnySpider(scrapy.Spider):
    name = 'ttfunnyspider'

    def __init__(self):
        self.start_urls = []

    def parse(self, response):
        print("")