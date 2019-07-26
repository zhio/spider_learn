# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibofansItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # actor_id = scrapy.Field()
    name = scrapy.Field()
    nike = scrapy.Field()
    actor_url = scrapy.Field()
    area = scrapy.Field()
    intro = scrapy.Field()
    guanzhu = scrapy.Field()
    fans = scrapy.Field()
    weibo_num = scrapy.Field()
    info = scrapy.Field()
