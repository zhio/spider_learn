'''
    头条科技爬虫 100条
    https://www.toutiao.com/ch/news_hot/

'''

import scrapy
import base64



class TouTiaoTechSpider(scrapy.Spider):
    name = 'tttechspider'

    def __init__(self):
        self.start_urls = []

    def parse(self, response):
        print("")