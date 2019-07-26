MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
REDIS_KEY = 'proxies'

import redis
from random import choice
class RedisClient(object):
    #初始化redis数据库
    def __init__(self,host = REDIS_HOST,port = REDIS_PORT,password = REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
    #向数据库中添加proxy
    def add(self,proxy,score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,{proxy:score})
    #从数据库中随机选择一个proxy
    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                return 0
    #当proxy不可用时进行分数减一或移除
    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减一')
            return self.db.zincrby(REDIS_KEY,-1,proxy)
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)
    #判断是否存在
    def exists(self,proxy):
        return not self.db.zscore(REDIS_KEY,proxy) == None
    #可用时设为最大值
    def max(self,proxy):
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})
    #统计
    def count(self):
        return self.db.zcard(REDIS_KEY)
    #获取全部代理
    def all(self):
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

    def batch(self,start,stop):
        return self.db.zrevrange(REDIS_KEY,start,stop-1)