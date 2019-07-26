'''
    头条娱乐新闻爬虫 100条
    https://www.toutiao.com/ch/news_entertainment/

'''

import scrapy
import base64



class TouTiaoEntertainmentSpider(scrapy.Spider):
    name = 'ttentertainmentspider'

    def __init__(self):
        self.start_urls = []

    def parse(self, response):
        print("")