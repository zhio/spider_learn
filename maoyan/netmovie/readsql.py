import pymysql
def sqlprint():
    connect = pymysql.connect(
                host='',
                port=3306,
                user='',
                passwd='',
                db='',
                charset='utf8')
    cursor = connect.cursor()
    cursor.execute('select id from maoyan_net_movie where category is not Null')
    d = cursor.fetchall()
    lists = list(d)
    list_mi = []
    s = 0
    for i in lists:
        for a in i:
            list_mi.append(a)
            s = s+1
    # print(list_mi)
    # a = list_mi[::2]
    # b = list_mi[1::2]
    # c = dict(zip(a, b))
    # # print(dict(zip(a,b)))
    # return c
    print(list_mi)
    print(s)
    return list_mi

sqlprint()
