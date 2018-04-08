# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import time

import redis
import scrapy

from scrapy.exceptions import DropItem

from tenement import settings


class TenementPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagesPipeline(object):
    def get_media_requests(self,item):
        for image_url in item['image_urls']:

            yield scrapy.Request(image_url)
    def item_completed(self,results ,item,info):
        image_paths=[x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item is contains no images')

        item['item_paths']=image_paths
        return item

# 小猪短租数据处理

class XiaoZhuPipeline(object):
    def __init__(self):
        self.file=codecs.open("xiaozhu_%s.json"%time.strftime('%Y%m%d',time.localtime()),'w',encoding='utf-8')
        if settings.REDIS_PASSWORD:
            self._db=redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,password=settings.REDIS_PASSWORD)
        else:
            self._db=redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT)
    def process_item(self,item,spider):
        data=json.dumps(dict(item),ensure_ascii=False)+'\n'
        print(data)
        if self._db.sismember('xiaozhu_data',item['address'])==0:
            self._db.sadd("xiaozhu_data",item['address'])
        self.file.write(data)
        return item
    def spider_closed(self,spider):
        self.file.close()