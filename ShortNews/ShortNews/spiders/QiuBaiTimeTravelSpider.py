'''
    糗百穿越（历史）爬虫 1000条
    https://www.qiushibaike.com/history/
'''

import scrapy
import base64
from ShortNews.items import ShortnewsInfoItem
from ShortNews.tool_hash import HashTool
import re

class QiuBaiTimeTravelSpider(scrapy.Spider):
    name = 'qbtimetravelspider'

    def __init__(self):
        self.hashs = HashTool()
        self.start_urls = ['https://www.qiushibaike.com/history/page/1/']
        for i in range(2, 14):
            self.start_urls.append('https://www.qiushibaike.com/history/page/{}/'.format(i))
        print(self.start_urls)
    def parse(self, response):
        flag = 1
        bodys = response.xpath('//div[@class = "article block untagged mb15"]').extract()
        i = 0
        for body in bodys:
            i = i +1
            content = re.findall('<div class="content"><span>(.*?)</span>',body,re.S)
            actor = re.findall('<h2>(.*?)</h2>',body,re.S)
            id = re.findall('<a href="/article/(.*?)" target="_blank" ',body,re.S)
            item = ShortnewsInfoItem()
            item['oid'] = id[0]
            item['title'] = actor[0].replace('\n', '')
            try:
                item['content'] = content[0].replace('\n', '')
            except:
                item['content'] = '暂无'
            item['platform'] = flag
            item['tag'] = 'TimeTrave'
            item['url'] = 'https://www.qiushibaike.com/article/' + item['oid']
            item['simhash'] = self.hashs.get_hash(item['content'])
            print(item)
            yield item