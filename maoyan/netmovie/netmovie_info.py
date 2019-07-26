import requests
import re
import json
import inproxy
import pymysql
import readsql
from lxml import etree

def get_page(id):
    user_agent = inproxy.user_agent()
    ip = inproxy.getRandomIP()
    proxy = {
        'HTTPS': ip
    }
    headers = {
        'User-Agent': user_agent,
    }
    get_key = requests.get('https://piaofang.maoyan.com/movie/'+str(id),headers=headers,proxies=proxy)

    return get_key


def parse_page(page):
    content = page.text
    html = etree.HTML(content)
    netMovie = {}
    try:
        netMovie["duration"] = html.xpath('//p[@class="info-duration ellipsis-1"]/text()')[0]
    except:
        netMovie["duration"] = '0'
    try:
        netMovie['info'] = re.findall('<div class="detail-block-content">(.*?)</div>', content, re.S)
    except:
        netMovie['info'] = ''

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
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def main():
    for id_sql in readsql.sqlprint():
        he=get_page(id_sql)
        data = parse_page(he)
        data['id'] = id_sql
        save_sql(data)


if __name__ == '__main__':
    main()

