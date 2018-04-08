# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TenementItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 标题
    title=scrapy.Field()
    # 价格
    price=scrapy.Field()
    #描述
    desc=scrapy.Field()
    #图片
    images=scrapy.Field()
    #优品
    superior_products=scrapy.Field()
    #速订
    book=scrapy.Field()
    # 商旅认证  Business travel certification
    BTC=scrapy.Field()
    # 常住
    Resident=scrapy.Field()
    #免押金
    free_deposit=scrapy.Field()
    # 验证
    validate=scrapy.Field()
    # 实拍
    shipai=scrapy.Field()
    # 门锁
    lock=scrapy.Field()
    #详细地址
    address=scrapy.Field()


