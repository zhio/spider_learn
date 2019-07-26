import requests
import json
import pymongo
def get_page(url):
    headers = {
        'User-Agent': 'baiduspider'
    }
    html = requests.get(url=url,headers=headers)
    print(html.text)
    return html.text

def parse_page(html):
    content = json.loads(html)
    datas = content.get('data')
    return datas

def save_mongo(dictitem):
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    mydb = myclient.manyan_rank
    mycol = mydb['hotman_douyin']
    mycol.insert_many(dictitem)

# url = 'https://box.maoyan.com/promarketing/api/netstar/rank/list.json?queryDate=20190312&rankType=0&netStarSource=1'
# get_page(url)
def main():
    queryDate = 20190331
    while queryDate >20190300:
        rankType = 0
        netStarSource = 1
        url = f'https://box.maoyan.com/promarketing/api/netstar/rank/list.json?queryDate={queryDate}&rankType={rankType}&netStarSource={netStarSource}'
        html = get_page(url)
        datas = parse_page(html)
        for data in datas:
            data['queryDate'] = queryDate
            print(data)
        save_mongo(datas)
        queryDate = queryDate-1

if __name__ == '__main__':
    main()