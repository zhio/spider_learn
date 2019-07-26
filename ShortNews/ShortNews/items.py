# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShortnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShortnewsInfoItem(scrapy.Item):
    #题目
    oid = scrapy.Field()
    title = scrapy.Field()
    #内容
    content = scrapy.Field()
    #喜欢数量
    likes = scrapy.Field()
    #评论数量
    comments = scrapy.Field()
    #分享数量
    shares = scrapy.Field()
    #不喜欢数量
    unlikes = scrapy.Field()
    #平台ID
    platform = scrapy.Field()
    #权重（给0）
    weight = scrapy.Field()
    #标签（如果有）
    tag = scrapy.Field()
    #url（原文地址/视频链接）
    url = scrapy.Field()
    #相似度hash表
    simhash = scrapy.Field()
