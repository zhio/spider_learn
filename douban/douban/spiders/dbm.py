# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import pymongo

class DbmSpider(scrapy.Spider):
    name = 'dbm'
    tags = ['电影', '电视剧', '综艺', '动漫', '纪录片', '短片']
    start = 0
    countries = ['中国大陆', '台湾', '香港']
    year_range = ['2019,2019', '2018,2018', '2010,2019', '2000,2009', '1990,1999', '1980,1989', '1970,1979',
                  '1960,1969', '1,1959']

    allowed_domains = ['douban.com']
    start_urls = []
    for i in range(5000):
        for tag in tags:
            for countrie in countries:
                for year in year_range:
                    page = i*20
                    URL = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&start={}&genres=%E5%89%A7%E6%83%85&countries={}&year_range={}'.format(tag,page,countrie,year)
                    start_urls.append(URL)
                    print(start_urls)

    def parse(self, response):
        print("hello")
        douban_json = json.loads(response.body)
        print(douban_json)
        douban_data=douban_json.get('data')
        myclient=pymongo.MongoClient(host='localhost',port=27017)
        mydb = myclient.test
        mycol = mydb.douban_movie
        for i in douban_data:
            mycol.update_one(i,{'$set':i},upsert=True)
            print(i)



