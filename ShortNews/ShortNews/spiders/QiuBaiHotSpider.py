'''
    糗百热门爬虫 1000条
    https://www.qiushibaike.com/
'''

import scrapy
import base64
import datetime


class QiuBaiHotSpider(scrapy.Spider):
    name = 'qbhotspider'

    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/8hr/page/{i}/' for i in range(11)]

    def parse(self, response):
        content_left_node = response.xpath("//div[@id='content-left']")  # 确定发布区的节点区域
        div_node_list = content_left_node.xpath("./div")
        for div_node in div_node_list:
            title_node = div_node.xpath(
                ".//div[@class='author clearfix']/a[contains(@onclick,'web-list-author-text')]/h2/text()")
            content_node = div_node.xpath(".//div[@class='content']/span[1]")
            content = content_node.xpath('string(.)')
            name = title_node.extract_first()
            info = content.extract_first()
            crawldate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item = {}
            item['name'] = name.strip() if name else name
            item['info'] = info.strip() if info else info
            item['crawldate'] = crawldate
            print (item)
            yield item