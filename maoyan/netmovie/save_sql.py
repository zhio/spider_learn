import pymysql
data={
    'id':"342873",
    'play_volume': '2060000000.0000002'

}
# def sqlsave(data):
#     db = pymysql.connect(host= '123.57.207.59',user='hheric',password='erichh',port=3306,db='fla_maoyan')
#     cursor =db.cursor()
#     table = 'maoyan_movie'
#     keys = ', '.join(data.keys())
#     values = ', '.join(['%s'] * len(data))
#
#     sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
#     update = ','.join([" {key} = %s".format(key=key) for key in data])
#     sql += update
#     try:
#         if cursor.execute(sql, tuple(data.values())*2):
#             print('Successful')
#             db.commit()
#     except:
#         print('Failed')
#         db.rollback()
#     db.close()
# sqlsave(data)

def save_sql1(data):
    db = pymysql.connect(host='', user='', password='', port=3306, db='')
    cursor = db.cursor()
    table = 'maoyan_typlay'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update

    if cursor.execute(sql, tuple(data.values()) * 2):
        print('Successful')
        db.commit()
    db.close()

save_sql1(data)
