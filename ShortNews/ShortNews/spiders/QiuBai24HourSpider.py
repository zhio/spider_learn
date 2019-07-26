'''
    糗百24小时（频道）爬虫 1000条
    https://www.qiushibaike.com/hot/
'''

import scrapy
import base64
import re
from ShortNews.tool_hash import HashTool
from ShortNews.items import ShortnewsInfoItem
class QiuBai24HourSpider(scrapy.Spider):
    name = 'qb24hourspider'

    def __init__(self):
        self.hashs = HashTool()
        self.start_urls = ['https://www.qiushibaike.com/hot/page/1/']
        for i in range(2,14):
            self.start_urls.append('https://www.qiushibaike.com/hot/page/{}/'.format(i))
        print (self.start_urls)

    def parse(self, response):
        bodys = response.xpath('//div[re:test(@id,"qiushi_tag_.*?")]').extract()
        flag = 1
        i = 0
        for body in bodys:
            i = i +1
            content = re.findall('<div class="content">\n<span>(.*?)</span>',body,re.S)

            actor = re.findall('<h2>(.*?)</h2>',body,re.S)
            id = re.findall('<a href="/article/(.*?)" target="_blank" ',body,re.S)
            item = ShortnewsInfoItem()
            item['oid'] = id[0]
            item['title'] = actor[0].replace('\n','')
            try:
                item['content'] = content[0].replace('\n','')
            except:
                item['content'] = '暂无'
            item['platform'] = flag
            item['tag'] = '24hours'
            item['url'] = 'https://www.qiushibaike.com/article/'+item['id']
            item['simhash'] = self.hashs.get_hash(item['content'])
            print(item)
            yield item
        print(i)

