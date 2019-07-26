#猫眼实时票房爬虫

import os
import requests
import json
import time 

#链接url
def get_to_link():
    try:
        r = requests.get("https://box.maoyan.com/promovie/api/box/second.json")
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("链接错误！！！")
        return ''

#json化字符串
def json_text(text):
    jd = json.loads(text)
    return jd

#返回实时日期
def date_time(jd):
    ja = jd['data']
    date = ja['queryDate']#返回日期
    alltime = ja['updateInfo'].split()[1]#返回时间
    money = ja['totalBox'] + ja['totalBoxUnit']#返回总票房
    return date,alltime,money

#返回影片票房
def movie_price(jd):
    jl = jd['data']['list']
    for i,jls in enumerate(jl,1):
        dic = {}
        dic['name'] = jls['movieName']#影片名
        try:
            dic['days'] = jls['releaseInfo'][2]#上映时间
        except:
            dic['days'] = '点映'
        
        dic['totalmoney'] = jls['sumBoxInfo']#影片总票房
        dic['mainmoney'] = jls['boxInfo']#综合票房
        dic['moneyrate'] = jls['boxRate']#票房占比
        dic['shownumber'] = jls['showInfo']#排片场次
        dic['showrate'] = jls['showRate']#排片占比
        dic['people'] = jls['avgShowView']#场均人次
        dic['showpeople'] = jls['avgSeatView']#上座率
        print(dic)


def main():
    html = get_to_link()
    text = json_text(html)
    movie_price(text)

if __name__ == "__main__":
    main()
