import requests
import re
import json
import inproxy
import pymysql
import readsql
def get_page(id):
    user_agent = inproxy.user_agent()
    headers = {
        'User-Agent': user_agent,
    }
    get_key = requests.get('https://piaofang.maoyan.com/movie/'+str(id),headers=headers)
    print(re.findall('<meta name="csrf" content="(.*?)" />',get_key.text))
    Uid = re.findall('<meta name="csrf" content="(.*?)" />', get_key.text)[0]
    ip = inproxy.getRandomIP()
    proxy = {
        'HTTPS': ip
    }
    headers_for_ajax = {
        'Referer': 'https://piaofang.maoyan.com/movie/'+str(id),
        'Uid': Uid,
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest'
    }
    base_url = 'https://piaofang.maoyan.com/netmovie/'

    page = requests.get(url= base_url+str(id)+'/boxinfo',headers = headers_for_ajax,proxies=proxy)
    return page


def parse_page(page):
    json_text = json.loads(page.text)
    html = json_text.get("boxInfoHtml")
    box_office = re.findall(r'累计分账.*?<span class="box-num">(.*?)</span>.*?累计观影人次',html,re.S)
    if len(box_office)>0:
        box_office_str = re.findall('累计分账.*?<span class="box-unit">(.*)</span>.*?累计观影人次',html,re.S)
        base = box_office[0]+box_office_str[0]
        base = str_to_float(base)
    else:
        base = '--'
        print(base)

    play_volume = re.findall(r'累计观影人次.*?<span class="box-num">(.*?)</span>.*?制作成本',html,re.S)
    if len(play_volume)>0:
        play_volume_str = re.findall('累计观影人次.*?<span class="box-unit">(.*)</span>.*?制作成本',html,re.S)
        base2 = play_volume[0]+play_volume_str[0]
        base2 = str_to_float(base2)
    else:
        base2 = '--'
        print(base2)

    cost=re.findall('制作成本.*<span class="box-num">(.*?)</span>',html,re.S)
    if len(cost):
        cost_str = re.findall('制作成本.*<span class="box-unit">(.*)</span>',html,re.S)
        base3 = cost[0]+cost_str[0]
        base3 = str_to_float(base3)
    else:
        base3 = '--'
        print(base3)

    netmovie = {}
    netmovie["box_office"] = base
    netmovie["play_volume"] = base2
    netmovie["cost"] = base3
    print(netmovie)
    return netmovie

def str_to_float(str_r):
    str_r = str_r.replace(',','')
    num=re.findall('(\d+(\.\d+)?)',str_r)[0][0]
    str_end = str_r[-1]
    if str_end == "万":
        str_end_int = 10000
    elif str_end == "亿":
        str_end_int = 10000*10000
    elif str_end == "千":
        str_end_int = 1000
    else:
        str_end_int = 1
    real_str = float(num)*str_end_int
    return real_str

def save_sql(data):
    db = pymysql.connect(host='123.57.207.59', user='hheric', password='erichh', port=3306, db='fla_maoyan')
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