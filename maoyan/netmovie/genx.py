import requests
import re
import json
import inproxy
import pymysql
import readsql
from lxml import etree
def aaa(id):
    headers_first = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    first = requests.get(url='https://piaofang.maoyan.com/movie/' + str(id), headers=headers_first)
    content = first.text
    response = etree.HTML(content)
    netMovie = {}
    netMovie["category"] = response.xpath('//span[@class="info-subtype ellipsis-1"]/text()')[0]
    if netMovie["category"] is not None:
        netMovie["category"] = netMovie["category"].replace("\n", "").replace(" ", "").replace("/", ",").strip()
    print(netMovie)
    return netMovie

def save_sql(data):
    db = pymysql.connect(host='', user='', password='', port=3306, db='')
    cursor = db.cursor()
    table = 'maoyan_net_movie'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    print(sql)
    print(data.values())
    if cursor.execute(sql, tuple(data.values()) * 2):
        print('Successful')
        db.commit()

    db.close()
def main():
    for id_sql in readsql.sqlprint():
        data = aaa(id_sql)
        data['id'] = id_sql
        print(data)
        save_sql(data)


if __name__ == '__main__':
    main()
