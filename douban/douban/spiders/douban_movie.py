import json
import time
import requests
import pymongo
from fake_useragent import UserAgent
from doubanproxy import getRandomIP,removeProxyIP
def get_proxy_ip():
    ip_port = requests.get("http://106.12.8.109:8000/get/").content.decode()
    proxies = {"https": "https://" + ip_port}
    return proxies
def crawl(urls,proxy = None,num_retries = 6):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    if proxy == None:
        try:
            response = requests.get(urls,headers = headers,timeout=5)
            time.sleep(1)
            data = response.json()['data']
            items = []
            for v in data:
                items.append(v)
            return items
        except:
            if num_retries>0:
                time.sleep(5)
                print('获取网页出错,5S后获取倒数第',num_retries,'次')
                crawl(urls,num_retries-1)
            else:
                print('开始使用代理')
                time.sleep(10)
                IP = getRandomIP()
                proxy = {
                    'https': IP,
                }
                crawl(urls,proxy)
    else:
        try:
            IP = getRandomIP()
            proxy = {'https':IP}
            response = requests.get(urls, headers=headers, proxies=proxy, timeout=5)
            data = response.json()['data']
            items = []
            for v in data:
                items.append(v)
            return items
        except:
            if num_retries>0:
                time.sleep(5)
                removeProxyIP(IP)
                IP = getRandomIP()
                proxy = {'https': IP}
                print("正在更换代理，10s后重新获取倒数第",num_retries,'次')
                print('当前代理是:',proxy)
                crawl(urls,proxy,num_retries-1)
            else:
                print('代理也不好用了！取消代理')
                return 0

def main():
    tags = ['电影', '电视剧', '综艺', '动漫', '纪录片', '短片']
    genres = ['情色','武侠','灾难','冒险','奇幻','西部','战争','历史','传记','歌舞','音乐','同性','犯罪','恐怖','惊悚','悬疑','动画','科幻','爱情','动作','喜剧','剧情']
    countries = ['中国大陆', '台湾', '香港','美国', '日本', '韩国','英国', '法国', '德国','意大利', '西班牙', '印度','泰国', '俄罗斯', '伊朗','加拿大', '澳大利亚', '爱尔兰','瑞典','巴西','丹麦']
    year_range = ['2019,2019', '2018,2018', '2010,2019', '2000,2009', '1990,1999', '1980,1989', '1970,1979','1960,1969', '1,1959']
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    mydb = myclient.test
    mycol = mydb.douban_china_00
    for tag in tags:
        total_tag = 0
        for countrie in countries:
            total_countris = 0
            for year in year_range:
                total_year = 0
                for genre in genres:
                    print("正在爬取",tag,countrie,genre,year,'下的数据')
                    url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&start={}&genres={}&countries={}&year_range={}'
                    start = 0
                    total = 0
                    while True:
                        urls = url.format(tag,start,genre,countrie,year)
                        items = crawl(urls)
                        if len(items)<=0:
                            break
                        info = {
                            'tag':tag,
                            'countrie':countrie,
                            'genre':genre,
                            'year':year
                        }
                        for item in items:
                            dictitem = dict( item, **info )
                            mycol.update_one(dictitem, {'$set': dictitem}, upsert=True)
                        start = start + 20
                        total += len(items)
                    print('已经抓取了{}电影信息'.format(total))
                total_year = total+total_year
            total_countris = total_countris + total_year
        total_tag = total_tag + total_countris
    print('总共抓取了{}条电影信息'.format(total_tag))

if __name__ == "__main__":
    main()