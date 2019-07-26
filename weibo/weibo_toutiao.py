import requests
import json
import pymysql
from bs4 import BeautifulSoup
import re
def get_list(page):
    headers = {
            "Host": "weibo.com",
            "Referer": "https://weibo.com/?category=1760",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
    }
    base_url = 'https://weibo.com/a/aj/transform/loadingmoreunlogin?&category=1760&page={}'.format(page)
    html = requests.get(url = base_url,headers = headers)
    weibo = json.loads(html.text)
    wb_html = weibo.get('data')
    weibo_ht = BeautifulSoup(wb_html,'lxml')
    weibo_class = weibo_ht.find_all('div',class_='UG_list_b')
    url_list = []
    for weibo_c in weibo_class:
        title = weibo_c.h3.string
        actor = weibo_c.find('span',class_='subinfo S_txt2').string
        url = weibo_c.find('a',class_='S_txt1').get("href")
        date = re.findall(r'''</a>\n<span class="subinfo S_txt2">(.*?)</span>\n<span class="subinfo_rgt S_txt2">''',str(weibo_c),re.S)
        num = re.findall(r'''<span class="subinfo_rgt S_txt2"><em class="W_ficon .*?</em><em>(.*?)</em></span>''',str(weibo_c),re.S)
        # print(title,actor,url,date[0],num[0],num[1],num[2])
        url_list.append(url)
    return url_list


def get_content(url):        
    headers = {
        "User-Agent":"baiduspider"
    }
    a = requests.get(url = url,headers = headers)
    soup = BeautifulSoup(a.text,'lxml')
    try:
        title = soup.find('div',class_ = 'title').string
        print(title)
        come_from = soup.find('em',class_='W_autocut').text
        weibo_time = soup.find('span',class_="time").text
        read_num = soup.find('span',class_='num').text
        try:
            actor = soup.find('em',class_='W_autocut').text
        except:
            actor = "作者未知"
        content = soup.find('div',class_='WB_editor_iframe_new').text
        print(come_from,weibo_time,read_num,actor,content)
        data = {}
        data['title'] = title
        data['content'] = content
        data['come_from'] = come_from
        data['weibo_time'] = weibo_time.replace("编辑于",'').replace(" ",'').replace("发布于",'')
        data['read_num'] = read_num.replace('阅读数：','')
        data['actor'] = actor
        data['url'] = url
        return data
    except:
        print('抱歉，该文章已被作者删除或暂无权限查看！')
        return None

def save_sql(data):
    db = pymysql.connect(host='123.57.207.59', user='hheric', password='erichh', port=3306, db='funshort')
    cursor = db.cursor()
    table = 'weibo_top'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()
'''
电影:10018
时尚:12
社会:7
头条:1760
热门:0
'''
def main():
    for i in range(1,1000):
        url_list = get_list(i)
        print(url_list)
        for url in url_list:
            data = get_content(url)
            if data is not None:
                save_sql(data)
if __name__ =="__main__":
    main()