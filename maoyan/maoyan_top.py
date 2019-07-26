import requests
import json
import re
import pymongo
def maoyan_top(year,num):
    headers = {
        "Host": "piaofang.maoyan.com",
        "Referer": "https://piaofang.maoyan.com/rankings/year",
        "Uid": "a28c0fb986ea655c13c861a9946f7fba430d02a7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    url = 'https://piaofang.maoyan.com/rankings/year?year='+str(year)+'&limit=100&tab='+str(num)
    print(url)
    response = requests.get(url = url,headers = headers)
    
    a = response.text
    print(a)
    maoyan = json.loads(a)
    text=maoyan.get("yearList")
    print(text)
    want = re.findall(r"""<ul class="row" data-com="hrefTo,href:'(.*?)'">
    <li class="col0">(.*?)</li>
    <li class="col1">
        <p class="first-line">(.*?)</p>
        <p class="second-line">(.*?) 上映</p>
    </li>
    <li class="col2 tr">(.*?)</li>
    <li class="col3 tr">(.*?)</li>
    <li class="col4 tr">(.*?)</li>
</ul>""",text,re.S)
    print(want)
    dic = {}
    dbs = "maoyan_top_" + str(year)
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    mydb = myclient.maoyan
    mycol = mydb[dbs]
    for val in want:
        dic['_id'] = val[1]
        dic['title'] = val[2]
        dic['data'] = val[3]
        dic['box_price'] = val[4]
        dic['price'] = val[5]
        dic['Number_of_people'] = val[6]
        dic['url'] = val[0]
        print(dic)
        mycol.update_one(dic, {'$set': dic}, upsert=True)

def main():
    lins = [0,2019,2018,2017,2016,2015,2014,2013,2012,2011]
    for num,year in enumerate(lins):
        print (num,year)
        maoyan_top(year,num)

if __name__ == "__main__":
    main()