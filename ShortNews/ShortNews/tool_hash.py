import math
import jieba
import jieba.analyse
import numpy as np

class HashTool(object):
    def __init__(self):
        pass

    def key_to_01(self,key):
        if key == "":
            return 0
        else:
            x = ord(key[0]) << 9
            m = 1000003
            mask = 2 ** 128 - 1
            for c in key:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(key)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]

            return str(x)

    def weight_to_01(self,weight):
        weight = weight*10 *10
        weight = round(weight)
        return weight

    def get_hash(self,text):
        seg_list = jieba.cut(text,cut_all=True)
        keywords = jieba.analyse.extract_tags("|".join(seg_list), topK=100, withWeight=True)
        ret = []
        for key,weight in keywords:
            key_01 = self.key_to_01(key)
            weight_01 = self.weight_to_01(weight)
            keylist = []
            for c in key_01:
                if c == "1":
                    keylist.append(int(weight_01))
                else:
                    keylist.append(-int(weight_01))
            ret.append(keylist)
        list1 = np.sum(np.array(ret), axis=0)

        simhash = ''
        for i in list1:
            if(i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def getDistince(self,hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1
        return length

a = HashTool()
s = a.get_hash("这是一句话")
print (s)