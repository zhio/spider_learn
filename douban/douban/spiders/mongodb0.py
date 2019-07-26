import pymongo
myclient = pymongo.MongoClient(host='localhost', port=27017)
mydb = myclient.test
mycol = mydb.douban_movie

import pymysql


connect = pymysql.connect(
    host='',
    port=3306,
    user='admin',
    passwd='admin',
    db='fla_maoyan',
    charset='utf8'
)

cursor = connect.cursor()
print("数据库打开")


# def save(item):
#     table = 'douban_movie'
#     keys = ', '.join(item.keys())
#     values = ', '.join(['%s'] * len(item))
#
#     sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
#                                                                                          values=values)
#     update = ','.join([" {key} = %s".format(key=key) for key in item])
#     sql += update
#
#     if cursor.execute(sql, tuple(item.values()) * 2):
#         print('Successful')
#         connect.commit()
#
#     print('Failed')
#     connect.rollback()
def save_mongo(item):
    mysave = mydb.douban_maoyan
    mysave.update_one(item, {'$set': item}, upsert=True)

a = mycol.find({"rate":{"$ne":''}},)
for i in a:

    try:
        rate = float(i['rate'])
    except:
        rate = 0
    try:
        star = int(i['star'])
    except:
        star = 0
    try:
        sql = 'SELECT movie_id FROM maoyan where name LIKE "{}" AND actor_name LIKE "{}"'.format(i['title'],i['directors'][0])
    except:
        sql = "SELECT movie_id FROM maoyan where name LIKE '{}'".format(i['title'])
    print(sql)

    cursor.execute(sql,())
    result = cursor.fetchall()
    if len(result) == 0:
        sql = 'SELECT movie_id FROM maoyan where name LIKE "{}"'.format(i['title'])
        cursor.execute(sql, ())
        result = cursor.fetchall()
    for dic in result:
        item = {
            'id':dic[0],
            'db_id':i['id'],
            'title':i['title'],
            'rate':rate,
            'star':star,
            'cover':i['cover'],
            'url':i['url'],
            'directors':i['directors'],
            'casts':i['casts']
        }
    save_mongo(item)
    print(item)





