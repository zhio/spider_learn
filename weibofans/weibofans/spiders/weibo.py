# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import WeibofansItem
from ..sqlprint import sqlprint
class WeiboSpider(scrapy.Spider):
    # actor = []
    # with open('China_actor.txt', 'r') as f:
    #     while True:
    #         lines = f.readline()
    #         if not lines:
    #             break
    #             pass
    #         lines = eval(lines)
    #         # print(lines)
    #         actor = actor + lines
    actor = sqlprint()
    print(actor)
    name = 'weibo'
    allowed_domains = ['weibo.com']
    # actor = ['陈国坤', '徐冬冬', '张雨绮', '郑恺', '张子君', '韩宇辰', '李牵', '王新军', '王珂', '李健', '周奇奇', '高瀚宇', '张俪', '彭小冉', '陈星旭', '刘帅', '丛健彰', '于和伟', '左小青', '周一围', '章子怡', '毛晓慧', '王劲松', '黄志忠', '胡歌', '郭媛媛', '白珊', '海一天', '何杜娟', '胡静', '邓伦', '张博', '罗晋', '王丽坤', '蒋恺', '焉栩嘉', '梁洁', '释小松', '刘威', '佟丽娅', '赵立新', '李一桐', '杨洋', '谷嘉诚', '秦昊', '李沁', '秦鸣悦', '王广源', '汤梦佳', '于谦', '金巴', '马可', '盖玥希', '彭昱畅', '侯明昊', '袁菲', '任泽巍', '佟大为', '孙俪', '赖艺', '白鹿', '易恒', '张哲华', '肖艺', '于春', '周梓言', '赵洪纪', '王春妹', '陈泽希', '郭子凡', '孟美岐', '梁靖康', '魏天浩', '宋轶', '陈学冬', '董岩磊', '卢星宇', '黄海冰', '吴倩', '张新成', '姜嫄', '曾淇', '丁禹兮', '何云龙', '梁海东', '窦新豪', '金士哲', '金钊', '王瑞雪', '刘婉婷', '赵芮', '田倚凡', '潘子剑', '何之舟', '叶小开', '朱丽岚', '张艺兴', '马精武', '黄晓明', '姚晨', '刘晓庆', '侯勇', '辛柏青', '李九霄', '唐艺昕', '梁静', '余皑磊', '魏晨', '张宥浩', '张俊一', '杜淳', '王婉娟', '李强', '于小伟', '王泷正', '阚清子', '孙艺洲', '王鸥', '张若昀', '张天其', '刘笑语', '谭俐敏', '李彤', '李成儒', '娟子', '程煜', '文静', '邓莎', '王子轩', '孙浩涪', '王庆祥', '吴国华', '陆思宇', '周依然', '谭希和', '杨新鸣', '陈牧扬', '许愿', '余心恬', '李珀', '彭高唱', '辣目洋子', '赵晓苏', '刘智扬', '胡可', '果静林', '沙溢', '冯嘉怡', '丁嘉丽', '汤唯', '崔新琴', '韩童生', '闫妮', '黄磊', '寇振海', '单思涵', '秦杉', '王梓权', '尹姝贻', '赵阳', '魏健隆', '赵达', '张大宝', '曹雷', '李宏磊', '吴明轩', '曹世平', '闫益民', '王军', '李骏林', '朱泳腾', '葛兆美', '张丹', '田瑞', '朱敏', '何小虎', '徐晟', '杜艳', '王璐', '蒋林燕', '范哲琛', '赵千紫', '刘钧', '岳旸', '李俊霆', '涂凌', '赵彦民', '红花', '王正权', '候长荣', '康群智', '王阳', '李燊', '许芳铱', '袁文康', '陈数', '童瑶', '潘粤明', '张彬彬', '杨幂', '李俊辰', '段小薇', '迟嘉', '张铭恩', '徐璐', '陈文波', '罗一航', '高毅', '满强', '蒋中炜', '陈升卫', '赵秋生', '韩银龙', '任希鸿', '薛勇', '周中和', '孙丹丹', '书亚信', '汪坚辛', '陆忠', '钟祺', '周建华', '洪士雅', '龙德', '胡小庭', '李进荣', '韩梦武', '谭建昌', '张弓', '赵韩樱子', '刘学', '郭伟', '师小红', '侯瑞祥', '容尔甲', '苏力德', '诺敏达莱', '宏通巴图', '斯力更', '彭信阳', '钢德尔', '安泽豪', '傅隽', '孙亦凡', '何志涛', '赵海鹰', '沈保平', '张春仲', '邓立民', '杜玉明', '谢雨辰', '张婉儿', '芦展翔', '韩昊霖', '李大光', '沈雪炜', '孙皓', '王婉晨', '孙子钧', '苗洛依', '邬靖靖', '孙逊', '陈剑', '宫正楠', '李东学', '曲吉', '贺刚', '黄骞', '郭军', '王德顺', '唐宁', '王鹏', '柳扬', '郭野', '朱嘉镇', '张银龙', '李曼铱', '胡帼雄', '徐爱珉', '于洋', '沈丹萍', '鲍大志', '谢宁', '高曙光', '孙浩', '马赫', '吴佩柔', '李万年', '何瑜', '孙桂田', '余玥', '周显欣', '李滨', '方子哥', '何中华', '钱泳辰', '付梦妮', '朱梓骁', '张予曦', '裴兴雷', '王堃', '黄维', '郭鹏', '金翀', '高媛', '黄雯', '那家威', '李彬硕', '刘蔚森', '陈霖生', '张恒平', '赵宁宇', '张辉', '杨紫茳', '王鑫', '李晓川', '李乃文', '姜峰', '江平', '扈强', '刚毅', '范奕泽', '巴特尔', '包贝尔', '涂门', '陈瑾', '谭凯', '何育骏', '左金珠', '王闯', '张帆', '郭涛', '乐思宏', '吕行', '邵晓薇', '冯玉香', '刘春霞', '薛亦伦', '宣璐', '袁冰妍', '成毅', '李若嘉', '张芷溪', '叶子诚', '龚锐', '方文强', '李欢', '邓郁立', '张樟', '孙嘉灵', '陈博豪', '李婷婷', '张超', '易国强', '虞荔', '王泽明', '于天川', '全保军', '王俊仁', '王欢', '芦永军', '沈凯', '李文豪', '王志刚', '许可', '韩红伟', '嘉男海林', '贾通波', '钟鑫培', '竺锦良', '陈家君', '金延虎', '徐立伟', '陈玥', '刘雨琨', '胡高峰', '宋凯', '程润坤', '鹿晗', '敖子逸', '肖战', '许凯', '杨弋墨', '田玲', '常戎', '马诗红', '高玉庆', '张光北', '杜旭东', '翟小兴', '楚建', '马维福', '苗亮', '郁晓东', '周晓海', '阮志强', '程希', '周杰', '金晖', '严志平', '吴任远', '冯晖', '顾士华', '刘根利', '夏志祥', '郑典', '梁丹妮', '徐纯学', '王雷', '康爱石', '徐玉琨', '李培铭', '徐僧', '白雪', '陆骏瑶', '王小橙', '常荻', '李博', '曹可凡', '张志忠', '任婉婧', '徐伟', '李耀强', '刘思纤', '余芷慧', '朱一文', '周毅', '曹阳', '王侃', '陈旭明', '张东', '阳光', '严米拉', '任学海', '王博', '胡彩虹', '李全有', '秦海璐', '胡明', '林辰涵', '蒋璐霞', '黄勐', '张皓承', '李光洁', '黄宥明', '张延', '孔琳', '姚橹', '刘蓓', '王锵', '钟楚曦', '胡晨曦', '大壮', '冯大路', '任山', '李如歌', '彭义程', '王若子', '刘南', '祝雨辛', '杨壹童', '赵蕴卓', '宁理', '贾景晖', '陈健飞', '傅晓娜', '刘牧梅', '黄晓娟', '吴连生', '周诗璇', '张译木', '李思博', '姚芊羽', '汪洋', '孙超', '白锦程', '李晓磊', '金有朋', '陈宝国', '徐哲', '柳雨明', '董春光', '岳俊岭', '刘波', '唐文琦', '蒋潇林', '闫巍', '冯凯', '秦隽哲', '胡力', '方帅', '彭理林', '王瑞', '崔晓天', '吴惠麟', '金玉倩', '梁栋才', '张帅奇', '刘立胜', '杨军']
    # starname = input("请输入名字：")
    # star = 'https://s.weibo.com/user?q='+starname
    start_urls = []
    for value in actor:
        # start_urls.append('https://s.weibo.com/user?q=演员' + value)
        start_urls.append('https://s.weibo.com/user?q='+ value )

    def parse(self, response):
        nike_name = response.xpath(
            '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/div/a[1]//text()').extract()
        name = response.xpath('//div[@class="search-input"]/input/@value').extract_first()
        flag = name.replace('演员','')
        if len(nike_name):

            nike_name = response.xpath(
                '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/div/a[1]//text()').extract()
            nike = ''.join(nike_name)
            actor_url=response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div/a/@href').extract_first()
            try:
                area = response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[1]/text()').extract()[1].strip()
            except:
                area = "未知"
            intro = response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[2]/text()').extract_first()
            if intro == '\n            ':
                intro = None
                guanzhu = response.xpath(
                    '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[2]/span[1]/a/text()').extract_first()
                fans = response.xpath(
                    '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[2]/span[2]/a/text()').extract_first()
                weibo_num = response.xpath(
                    '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[2]/span[3]/a/text()').extract_first()
                info = response.xpath(
                '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"][1]/p[3]//text()').extract_first()

            else:
                guanzhu = response.xpath(
                    '//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[3]/span[1]/a/text()').extract_first()
                fans =response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[3]/span[2]/a/text()').extract_first()
                weibo_num =response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"]/p[3]/span[3]/a/text()').extract_first()
                info = response.xpath('//div[@class="card card-user-b s-pg16 s-brt1"][1]/div[@class="info"][1]/p[4]//text()').extract_first()
            if info == "标签：" or info == "教育信息：" or info == "职业信息：":
                info = None
            # print("昵称：",nike)
            # print("主页：",actor_url)
            # print(area)
            # print(intro)
            # print("关注：",guanzhu)
            # print("粉丝",fans)
            # print("微博数：",weibo_num)
            # print(info)
            actor_id = list(self.actor.keys())[list(self.actor.values()).index(flag)]
            if intro is not None:
                if len(re.findall('演',intro)) or len(re.findall('艺',intro)) or len(re.findall('剧',intro)) or len(re.findall('歌',intro)) or (fans.find("万")>0 and len(fans)>2):

                    items = WeibofansItem()
                    # items['actor_id'] = actor_id
                    items['name'] = name
                    items['nike'] = nike
                    items['actor_url'] = actor_url
                    items['area'] = area
                    items['intro'] = intro
                    items['guanzhu'] = guanzhu
                    items['fans'] = fans
                    items['weibo_num'] = weibo_num
                    items['info'] = info
                    yield items
                    print(items)
                else:
                    print("没有找到符合规则的人"+name)
            elif fans.find("万")>0 and len(fans)>2:
                items = WeibofansItem()
                # items['actor_id'] = actor_id
                items['name'] = name
                items['nike'] = nike
                items['actor_url'] = actor_url
                items['area'] = area
                items['intro'] = intro
                items['guanzhu'] = guanzhu
                items['fans'] = fans
                items['weibo_num'] = weibo_num
                items['info'] = info
                yield items
                print(items)
            else:
                print("没有找到"+name+"的微博")
        else:
            print("没有找到" + name + "的微博")



