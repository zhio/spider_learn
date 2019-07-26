import json
import requests

import pymongo
from spiders.doubanproxy import getRandomIP,removeProxyIP
def crawl(urls):
    ip = getRandomIP()
    proxy = {
        'http':'http://'+ip,
        'https':'https://'+ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    }
    print(urls)
    response = requests.get(urls,headers = headers,proxies=proxy)
    if response.status_code != 200:
        raise Exception('http status code is {}'.format(response.status_code))

    data = response.json()['data']
    items = []
    for v in data:
        items.append(v)
    return items

def main():
    tags = ['电影', '电视剧', '综艺', '动漫', '纪录片', '短片']
    genres = ['情色','武侠','灾难','冒险','奇幻','西部','战争','历史','传记','歌舞','音乐','同性','犯罪','恐怖','惊悚','悬疑','动画','科幻','爱情','动作','喜剧','剧情']
    countries = ['中国大陆', '台湾', '香港']
    year_range = ['2019,2019', '2018,2018', '2010,2019', '2000,2009', '1990,1999', '1980,1989', '1970,1979',
                  '1960,1969', '1,1959']
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    mydb = myclient.test
    mycol = mydb.douban_movie
    for tag in tags:
        for countrie in countries:
            for year in year_range:
                url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&start={}&countries={}&year_range={}'
                start = 0
                total = 0
                while True:
                    print(url.format(tag,start,countrie,year))
                    urls = url.format(tag,start,countrie,year)
                    print(urls)
                    items = crawl(urls)
                    if len(items)<=0:
                        break
                    for item in items:
                        print(item)
                        mycol.update_one(item, {'$set': item}, upsert=True)
                    start = start + 20
                    total += len(items)
                    print('已经抓取了{}电影信息'.format(total))
    print('总共抓取了{}条电影信息'.format(total))

if __name__ == "__main__":
    main()