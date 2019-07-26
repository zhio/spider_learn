# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from ShortNews.items import ShortnewsInfoItem
class ShortnewsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='',
            port=3306,
            user='',
            passwd='',
            db='',
            charset='utf8'
        )

    def open_spider(self, spider):
        self.cursor = self.connect.cursor()
        print("数据库开启")

    def process_item(self, item, spider):
        table = 'short_news'
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in item])
        sql += update

        if self.cursor.execute(sql, tuple(item.values()) * 2):
            #print('Successful')
            self.connect.commit()
        # except:
        #     #print('Failed')
        #     self.connect.rollback()

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
        print("数据库关闭")
