import requests
import json
import re
import pymysql
import datetime
def get_page(url):
    headers = {
        'User-Agent':'BaiduSpider'
    }
    html = requests.get(url,headers = headers,verify=False).text
    datas = json.loads(html)
    data = datas.get('data')
    return data

def save_data(data,url):
    for i in data:
        data_dic = {}
        data_dic = i
        data_dic['datefrom'] = re.findall('queryDate=(.*)',url)[0]
        yield data_dic

def save_sql(datas,tables):
    connect = pymysql.Connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        db = 'fla_maoyan',
        charset = 'utf8mb4'
    )
    cursor = connect.cursor()
    for data in datas:
        table = tables
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table,keys=keys,values=values)
        update = ','.join([" {key}=%s".format(key=key) for key in data])
        sql += update
        if cursor.execute(sql,tuple(data.values())*2):
            print('Successful')
            connect.commit()
        # try:
        #     if cursor.execute(sql,tuple(data.values())*2):
        #         print('Successful')
        #         connect.commit()
        # except:
        #     print('Failed')
        #     connect.rollback()
    cursor.close()
    connect.close()
    print("数据库关闭")
def get_nday_list(n):
    before_n_days = []
    for i in range(1,n+1)[::-1]:
        before_n_days.append(str(datetime.date.today()-datetime.timedelta(days=i)).replace('-',''))
    return before_n_days
def main():
    url = 'https://box.maoyan.com/promarketing/api/netstar/rank/list.json?rankType=2&netStarSource=1&queryDate=20190711'
    html = get_page(url)
    data_dic = save_data(html,url)
    tables = 'TikTok_fans'
    save_sql(data_dic,tables)
if __name__ == "__main__":
    main()