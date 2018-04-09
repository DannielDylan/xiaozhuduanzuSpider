# -*- coding:utf-8 -*-
# @Date   : 2018/4/8 0008
# @Author : Dylan
# @File   : ziru.p
import json
import re

import requests
import time

from lxml import etree
from selenium import webdriver

"""
测试代码
:return:


driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
driver.find_element_by_id('kw').send_keys('自如')
driver.find_element_by_id('su').click()
time.sleep(2)
driver.save_screenshot('./自如.png')
time.sleep(10)
print(driver.page_source)
# print(driver.get_cookie())
cookies={i['name']:i['value'] for i in driver.get_cookie()}
print(cookies)
driver.quit()
"""


class ZRSpider:
    def __init__(self):
        self.city_name=input('请输入区域/地铁/小区的缩写英文字母开始找房:')
        self.start_url = 'http://{}.ziroom.com/z/nl/z3.html?'.format(self.city_name)
        self.headers = {
            'Accept': 'application / json, text / javascript, * / *; q = 0.01',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            # 'Connection': 'keep - alive',
            # 'Host': 'search.ziroomstay.com',
            # 'Referer': 'http://search.ziroomstay.com/search/rooms?cityCode=310000',
            # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36p: 5'
        }
        self.temp_url=self.start_url+'p={}'

        self.url_list = [self.temp_url.format(i) for i in range(1, 51)]

    def get_url(self, url):
        # for n in range(50):
        #     url_list=self.start_url+"p={}".format(n)
        response = requests.get(url, headers=self.headers, timeout=3)

        return response.content.decode()
    def parse_url(self,url):
        try:
            html_str=self.get_url(url)
        except Exception as e:
            print(e)
            html_str=None
        return html_str




    def get_content_list(self,html_str):

        content_list=[]
        if html_str is not None:

            html=etree.HTML(html_str)

            # infos=html.xpath('//div[@class="t_newlistbox"]/ul/li')[1:]
            infos=html.xpath('//div[@class="t_newlistbox"]/ul/li')

            for li in infos:
                item={}
                # 详情页
                item['details_page']=li.xpath('./div[1]/a/@href')
                # 标题
                item['title']=li.xpath('./div[2]/h3/a/text()')
                # 位置
                item['position']=li.xpath('.//div[2]/h4/a/text()')
                # 楼层
                item['detail_floor']=li.xpath('./div[2]/div/p[1]/span/text()')
                # 距离
                item['distance']=li.xpath('./div[2]/div/p[2]/span/text()')
                item['price']=li.xpath('./div[3]/p[1]/text()')

                #替换价格中的空字符串
                item['price']=''.join(item['price']).strip()

                # room_tags
                # isinstance(subway)
                item['subway']=li.xpath('./div[2]/p/span[1]/text()')
                item['subway']=item['subway'][0] if len(item['subway'])>0 else None
                # Independentbalcony
                item['balcony']=li.xpath('./div[2]/p/span[2]/text()')
                item['balcony']=item['balcony'][0] if len(item['balcony'])>0 else None
                # bed for style
                item['bed_style']=li.xpath('./div[2]/p/span[3]/text()')
                item['bed_style']=item['bed_style'][0] if len(item['bed_style'])>0 else None
                content_list.append(item)
            # next_url=html.xpath('//*[@id="page"]/a[9]/@href')
            print(content_list)
            return content_list
    def parse_detail_page(self, content_list):

        # for url in content_list:
        #     if isinstance(url,dict):
        #         for k,v in url.items():
        #             print(v)


        file_path="ziru_{}.txt".format(self.city_name)
        with open(file_path,'w',encoding='utf-8') as f:
            for i in range(len(content_list)):
                temp_url = content_list[i]['details_page']
                # print(temp_url)
                detail_url = "http:" + ''.join(temp_url)

                detail_html=requests.get(detail_url,headers=self.headers,timeout=5).content.decode()
                #太长了标题  这这先缩写下detail_html=infos
                # detail_infos=etree.HTML(detail_html)
                infos=etree.HTML(detail_html)
                img_list=infos.xpath('//*[@id="cao"]/ul/li/a/@href')
                # total_img_list.extend(img_list)
                content_title=infos.xpath('//div[@class="room_detail_left"]/div[2]/h2/text()')

                # content_id=infos.xpath('//div[@class="room_detail_left"]/div[3]/h3/text()')
                # content_id=infos.xpath('//div[@class="room_detail_left"]/div[3]')

                # content = infos.xpath('//div[5]/div[1]/div[3]/p')  只能取p
                content = infos.xpath('//div[@class="room_detail_left"]/div[3]/descendant::text()')
                content = ''.join(content)
                # content=infos.xpath('//div[@class="room_detail_left"]/div[3]/p/text()')
                house_config=infos.xpath('//div[@class="room_detail_left"]/div[5]/ul/li/text()')

                # paycon=infos.xpath('//tr[td]')
                paycon = infos.xpath('//td/text()|//td/span/text()')

            # detail_list=("图片:"+%s+','+'内容标题:'+%s+','+'编号:'+%s+','+'内容:'+%s+','+'房屋配置:'+%s+','+'付费方式:'+%s)%(img_list,content_title,content_id,content,house_config,paycon)
                f.write("{},{},{},{},{}".format(img_list,content_title,content,house_config,paycon)+'\n')
                print('保存成功')

    def save_content_list(self, content_list):
        file_path="{}.txt".format(self.city_name)
        with open(file_path,'a') as f:
            for con in content_list:
                f.write(json.dumps(con,ensure_ascii=False,indent=2))
                f.write('\n')
        print("保存成功")

        #     for con in detail_list:
        #         f.write(json.dumps(con, ensure_ascii=False, indent=2))
        #         f.write('\n')
        # print("保存成功")




    # driver.quit()

    def run(self):
        # print(1,self.url_list)
        # for n in range(50):
        #     self.url = "http://search.ziroomstay.com/search/list?cityCode=310000&page={}&priceStart=0".format(n)
        for i in range(len(self.url_list)):
            for url in self.url_list:
                html_str = self.get_url(url)
                content_list=self.get_content_list(html_str)
                # detail_list=self.parse_detail_page(content_list)
                self.parse_detail_page(content_list)
                self.save_content_list(content_list)

        # print(html_str)
        # with open('1.html', 'w') as f:
        #     f.write(html_str)


if __name__ == '__main__':
    ziru = ZRSpider()
    ziru.run()
