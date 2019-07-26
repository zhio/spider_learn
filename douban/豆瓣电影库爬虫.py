import json
import time
import requests
import pymongo
from fake_useragent import UserAgent
from doubanproxy import getRandomIP,removeProxyIP

def crawl(urls):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    response = requests.get(urls, headers=headers)
    data = response.json()['data']
    items = []
    for v in data:
        items.append(v)
    return items
    # try:
    #     IP = getRandomIP()
    #     proxy = {'https':"https://"+IP}
    #     response = requests.get(urls, headers=headers, proxies=proxy, timeout=5)
    #     data = response.json()['data']
    #     items = []
    #     for v in data:
    #         items.append(v)
    #     return items
    # except:
    #     removeProxyIP(IP)
    #     items = crawl(urls)
    #     return items

def main():
    a = 0
    tags = ['电影', '综艺', '动漫', '纪录片', '短片']
    genres = ['情色','武侠','灾难','冒险','奇幻','西部','战争','历史','传记','歌舞','音乐','同性','犯罪','恐怖','惊悚','悬疑','动画','科幻','爱情','动作','喜剧','剧情']
    countries = ['中国大陆', '台湾', '香港','美国', '日本', '韩国','英国', '法国', '德国','意大利', '西班牙', '印度','泰国', '俄罗斯', '伊朗','加拿大', '澳大利亚', '爱尔兰','瑞典','巴西','丹麦']
    year_range = ['2019,2019', '2018,2018', '2010,2019', '2000,2009', '1990,1999', '1980,1989', '1970,1979','1960,1969', '1,1959']
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    mydb = myclient.test
    mycol = mydb.douban78
    for tag in tags:
        for countrie in countries:
            for year in year_range:
                for genre in genres:
                    if tag=='电影' and genre=='惊悚' and countrie =='美国' and year=='2010,2019':
                        a = 1
                        print("现在开始爬去")
                    if a == 1:
                        print("正在爬取",tag,countrie,genre,year,'下的数据')
                        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&start={}&genres={}&countries={}&year_range={}&limit=100'
                        start = 0
                        total = 0
                        while True:
                            urls = url.format(tag,start,genre,countrie,year)
                            try:
                                items = crawl(urls)
                            except:
                                print(urls)
                                break
                            if len(items) <= 0:
                                break
                            info = {
                                'tag':tag,
                                'countrie':countrie,
                                'genre':genre,
                                'year':year
                            }

                            for item in items:
                                print(item['title'])
                                dictitem = dict( item, **info )
                                mycol.update_one(dictitem, {'$set': dictitem}, upsert=True)
                            start = start + 100
                            total += len(items)
                        print('已经抓取了{}电影信息'.format(total))

if __name__ == "__main__":
    main()