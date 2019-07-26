'''
    糗百新鲜爬虫 1000条
    https://www.qiushibaike.com/textnew/
'''

import scrapy
import base64
import re
from ShortNews.items import ShortnewsInfoItem
from ShortNews.tool_hash import HashTool

class QiuBaiFreshSpider(scrapy.Spider):
    name = 'qbfreshspider'

    def __init__(self):
        self.hashs = HashTool()
        self.start_urls = ['https://www.qiushibaike.com/textnew/page/1/']
        for i in range(2,32):
            self.start_urls.append('https://www.qiushibaike.com/textnew/page/{}/'.format(i))
        print (self.start_urls)

    def parse(self, response):
        flag = 1
        print('运行到这里了')
        print(response.body)
        bodys = response.xpath('//div[@class="article block untagged mb15"]').extract()
        print(bodys)
        i = 0
        for body in bodys:
            i = i +1
            content = re.findall('<div class="content">.*?<span>(.*?)</span>',body,re.S)
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
            item['tag'] = 'Fresh'
            item['url'] = 'https://www.qiushibaike.com/article/' + item['id']
            item['simhash'] = self.hashs.get_hash(item['content'])
            print(item)
            yield item
