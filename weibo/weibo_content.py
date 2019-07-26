import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent":"baiduspider"
}
a = requests.get('http://t.cn/EoQqfT9',headers = headers)
print(a.text)
soup = BeautifulSoup(a.text,'lxml')
print(soup)
title = soup.find('div',class_ = 'title').string
print(title)
come_from = soup.find('em',class_='W_autocut').text
weibo_time = soup.find('span',class_="time").text
read_num = soup.find('span',class_='num').text 
preface = soup.find('div',class_='preface').text
content = soup.find('div',class_='WB_editor_iframe_new').text
print(come_from,weibo_time,read_num,preface,content)
