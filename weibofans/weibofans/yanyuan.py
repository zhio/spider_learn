import urllib.request
from lxml import etree
# response = urllib.request.urlopen('http://www.manmankan.com/dy2013/mingxing/yanyuan/')
# data =response.read().decode('utf-8')
# html = etree.HTML(data)
# html = html.xpath('//div[@id="mx_con1"]//text()')
# print(html)
# for i in html:
#     if i == '\n':
#         html.remove(i)
# print(html)
# print(len(html))
import re
s = "p演员，代表作品《独步天下》《军师联盟》《甄嬛传》《诛仙》等"
a = re.findall('演员',s)
print(len(a))




