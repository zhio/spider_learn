import requests
import json
import pymysql
def get_page(url):
    headers = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    baseurl = 'https://aweme-hl.snssdk.com/aweme/v1/hotsearch/star/list/?count=50&offset='
    url = baseurl + str(url) +'&sort_type=2&type=1'
    print(url)
    html = requests.get(url= url,verify =  False )
    print(url)
    return html

def parse_page(html):
    hjson = json.loads(html.text)
    #douyin = re.compile('.*?"followers":(.*),.*?',html.text)
    star_list=hjson['star_list']
    for i in range(0,50):
        followers=star_list[i]['followers']
        nickname = star_list[i]['user_info']['nickname']
        signature = star_list[i]['user_info']['signature']
        uid = star_list[i]['user_info']['uid']
        avatar_larger = star_list[i]['user_info']['avatar_larger']['url_list'][0]
        print(nickname)
        item = {
            'uid':uid,
            'nickname' : nickname,
            'followers': followers,
            'avatar_larger':avatar_larger,
            'signature' : signature
        }
        save_page(item)

def save_page(data):
    db = pymysql.connect(host='123.456.78.90', user='root', password='root', port=3306, db='spider')
    cursor = db.cursor()
    table = 'douyin'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()

def main():
    for a in range(0,100):
        a = a*50
        html =get_page(a)
        parse_page(html)

main()

