import pymysql
def sqlprint():
    connect = pymysql.connect(
                host='你的数据库地址',
                port=3306,
                user='你的数据库名称',
                passwd='你的数据库密码',
                db='maoyan',
                charset='utf8')
    cursor = connect.cursor()
    cursor.execute('select * from actors')
    d = cursor.fetchall()
    lists = list(d)
    list_mi = []
    for i in lists:
        for a in i:
            list_mi.append(a)
    # print(list_mi)
    a = list_mi[::2]
    b = list_mi[1::2]
    c = dict(zip(a, b))
    # print(dict(zip(a,b)))
    return c

sqlprint()

