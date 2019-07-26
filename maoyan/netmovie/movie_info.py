import requests
import re
import json
import pymysql

def get_page(id):
    headers = {
        # 'Referer': 'https://piaofang.maoyan.com/movie/'+str(id),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        # 'Uid':'bf63507847c08aa9b01615bc6ef4942d28af2b01',
        # 'X-Requested-With': 'XMLHttpRequest'
    }
    base_url = 'https://piaofang.maoyan.com/movie/'
    page = requests.get(url= base_url+str(id)+'/moresections',headers = headers)
    return page

def parse_page(page):
    json_text = json.loads(page.text)
    info = json_text['sectionHTMLs']["detailSection"]
    html = info.get('html')
    info_movie = re.findall('class="detail-block-content">(.*?)</div>',html)
    print(info_movie)
    return info_movie

def save_sql(data):
    db = pymysql.connect(host='', user='', password='', port=3306, db='')
    cursor = db.cursor()
    table = 'maoyan_movie'
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
    for id in range(10,100):
        html = get_page(id)
        info = parse_page(html)
        data = {
            'id' : id,
            'info':info
        }
        save_sql(data)

if __name__ == '__main__':
    main()
