import requests
import re
import base64
from fontTools.ttLib import TTFont
from lxml import etree

import pymysql
import readsql
def save_xml():
    font = "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"
    fontdata = base64.b64decode(font)
    with open("maoyan.woff", "wb") as f:
        f.write(fontdata)
    maoyan_fonts = TTFont('maoyan.woff')
    maoyan_fonts.saveXML("text.xml")


def get_rel():
    maoyan_fonts = TTFont('maoyan.woff')
    font_dict = {}
    base_num = {
        "uniF1D0": "4", "uniE13A": "3", "uniE64F": "0", "uniECF2": "1", "uniF382": "2",
        "uniE1FD": "8", "uniF5E4": "6", "uniF1B0": "9", "uniE71E": "7", "uniE979": "5"}
    _data = maoyan_fonts.getGlyphSet()._glyphs.glyphs
    for k, v in base_num.items():
        font_dict[_data[k].data] = v
    return font_dict


def get_woff(font_text):
    base64_behind = re.split('\;base64\,', font_text)[1]
    font_content = re.split('\)', base64_behind)[0].strip()
    if font_content:
        bs_font = base64.b64decode(font_content)
        with open("new.woff", 'wb') as f:
            f.write(bs_font)
    font_ttf = TTFont("new.woff")
    data = font_ttf.getGlyphSet()._glyphs.glyphs
    return data


# 将文字替换成数字
def replace_Str(str_r, data_woff):
    font_dict = get_rel()
    if str_r[-1] == "万" or str_r[-1] == "%" or str_r[-1] == "亿":
        str_end = str_r[-1]
        string = str_r.replace("万", '').replace("%", "").replace("亿", "")
        num_list = string.split(";")
        str_All = ""
        for each_str in num_list:
            if not each_str.startswith("."):
                each_str = each_str[3:].upper()
                if each_str:
                    each_str = font_dict[data_woff["uni%s" % each_str].data]
                    str_All += each_str
            else:
                str_All += '.'
                each_str = each_str[4:].upper()
                each_str = font_dict[data_woff["uni%s" % each_str].data]

                str_All += each_str

        str_All += str_end
        return str_All
    else:
        str_list = str_r.split(";")
        str_All = ""
        for each_str in str_list:
            if each_str and not each_str.startswith("."):
                each_str = each_str[3:].upper()
                each_str = font_dict[data_woff["uni%s" % each_str].data]
                str_All += each_str
            elif each_str:
                str_All += '.'
                each_str = each_str[4:].upper()
                each_str = font_dict[data_woff["uni%s" % each_str].data]
                str_All += each_str
        return str_All
def str_to_float(str_r):
    str_r = str_r.replace(',','')
    num=re.findall('(\d+(\.\d+)?)',str_r)[0][0]
    str_end = str_r[-1]
    if str_end == "万":
        str_end_int = 10000
    elif str_end == "亿":
        str_end_int = 10000*10000
    elif str_end == "千":
        str_end_int = 1000
    else:
        str_end_int = 1
    real_str = float(num)*str_end_int
    return real_str

def save_sql(data):
    db = pymysql.connect(host='123.57.207.59', user='hheric', password='erichh', port=3306, db='fla_maoyan')
    cursor = db.cursor()
    table = 'maoyan_tvplay'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    print(sql)
    print(data.values())
    if cursor.execute(sql, tuple(data.values()) * 2):
        print('Successful')
        db.commit()

    db.close()

save_xml()
def get_page(id):
    headers_first = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
                  }
    first = requests.get(url = 'https://piaofang.maoyan.com/movie/'+str(id),headers = headers_first)
    content = first.text
    html = etree.HTML(content)
    try:
        font_text = html.xpath('//style[@id="js-nuwa"]/text()')[0]
        data_woff = get_woff(font_text)
        print('成功')
    except:
        print("失败")

    resultList = re.findall('<p class="heat-value">(.*?)</p>',content,re.S)
    if len(resultList) > 0:
        piaof = resultList[-1]
    # 累计播放量
    resultList = re.findall('累计播放量.*?含爱奇艺预估.*?<i class="cs">(.*?)</i></span>', content, re.S)
    if len(resultList) > 0:
        piaof = resultList[0]
    else:
        resultList = re.findall('累计播放量.*?<i class="cs">(.*?)</i></span>',content,re.S)
        if len(resultList) > 0:
            piaof = resultList[0]
    resultList = re.findall('累计播放量.*?<i class="cs">.*?</i></span><span class="box-unit">(.*?)</span>', content, re.S)
    if len(resultList) > 0:
        piaof = piaof + resultList[0]
        try:
            data_woff = get_woff(font_text)
            play_volume  = replace_Str(piaof , data_woff)
            piaof = play_volume
        except:
            print("【错误】字体解析失败")
    play = {}
    play['play_volume'] = str_to_float(piaof)
    return play

def main():
    for id_sql in readsql.sqlprint():
        data = get_page(id_sql)
        data['id'] = id_sql
        print(data)
        save_sql(data)


if __name__ == '__main__':
    main()