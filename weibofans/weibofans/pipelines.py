# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weibofans.items import WeibofansItem

class WeibofansPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='123.45.678.90',
            port=3306,
            user='root',
            passwd='root',
            db='spider',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        table = 'weibo_all_people'
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in item])
        sql += update
        # if self.cursor.execute(sql, tuple(item.values()) * 2):
        #     print('Successful')
        #     self.connect.commit()
        # except :
        #     print('Failed')
        #     self.connect.rollback()
        try:
            if self.cursor.execute(sql, tuple(item.values()) * 2):
                print('Successful')
                self.connect.commit()
        except:
            print('Failed')
            self.connect.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
