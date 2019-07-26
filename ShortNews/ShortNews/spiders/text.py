import requests
import json
import pymysql
import time
import random
from ShortNews.tool_hash import HashTool
def get_page(i):
    hashs = HashTool()
    headers = {
        # 'GET' :'/article/list/text?count=30&page=1 HTTP/1.1',
        'Host':'m2.qiushibaike.com',
        # 'Source':'ios_11.8.0',
        # 'Accept':'*/*',
        # 'app':'1',
        'Uuid':'ios_1e111a1d65d34295b21321e18671b97e',
        # 'screen':'414,736',
        # 'qbaid':'D5B0B037-0DF9-410C-B3E9-4C1AB8A55C6B',
        # 'User-Agent':'QiuBai/11.8.0 rv:31 (iPhone; iOS 11.1; zh_CN) PLHttpClient/1_WIFI',
        # 'Accept-Language':'zh-Hans-CN;q=1',
        # 'Accept-Encoding':'br, gzip, deflate',
        # 'Connection':'keep-alive'
    }
    url = 'https://119.29.47.97/article/list/text?count=30&page='+str(i)
    a=requests.get(url = url,headers = headers,verify = False)
    b = json.loads(a.text)
    items = b['items']

    for item in items:
        item_dic = {}
        formats = item['format']
        content = item['content']
        comments = item['comments_count']
        id = item['id']
        down = item['votes']['down']
        up = item['votes']['up']
        # user = item['user']['login']
        # astrology = item['user']['astrology']
        # user_id = item['user']['uid']
        # gender = item['user']['gender']
        # age = item['user']['age']
        share_count = item['share_count']
        item_dic['tag'] = formats
        item_dic['content'] = content
        item_dic['comments'] = comments
        # item_dic['types'] = types
        item_dic['oid'] = id
        item_dic['unlikes'] = -down
        item_dic['likes'] = up
        item_dic['title'] = ''
        item_dic['shares'] = share_count
        item_dic['url'] = 'https://www.qiushibaike.com/article/'+str(id)
        item_dic['simhash'] = hashs.get_hash(content)
        item_dic['platform'] = 1
        item_dic['weight'] = 0
        print(content)
        # item_dic['astrology'] = astrology
        # item_dic['user_id'] = user_id
        # item_dic['gender'] = gender
        # item_dic['age'] = age
        save_sql(item_dic)

def save_sql(data):
    db = pymysql.connect(host='123.57.207.59', user='hheric', password='erichh', port=3306, db='funshort')
    cursor = db.cursor()
    table = 'short_news'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def main():
    for i in range(1,1000):
        get_page(i)
        time_to_sleep = random.randint(1, 10)
        print('等待',time_to_sleep,'秒')
        time.sleep(time_to_sleep)

if __name__ == "__main__":
    main()