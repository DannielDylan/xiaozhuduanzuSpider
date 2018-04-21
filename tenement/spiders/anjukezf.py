# -*- coding: utf-8 -*-
import re

import scrapy
from tenement.items import AnJuKezfItem

class AnjukezfSpider(scrapy.Spider):
    name = 'anjukezf'
    allowed_domains = ['anjuke/fangyuan.com']
    start_urls = ['https://hz.zu.anjuke.com/fangyuan']
    custom_settings = {
        'ITEM_PIPELINES': {
            'tenement.pipelines.TenementPipeline': 300,
            'tenement.pipelines.AnJuKePipeline': 350,

        },
        'DOWNLOADER_MIDDLEWARES': {
            'tenement.middlewares.TenementSpiderMiddleware': 543,
            'tenement.middlewares.IPProxiesMiddleware': 565,
            'tenement.middlewares.RandomUserAgent': 560,

            # 使用scrapy_crawlera 就可以将之前设置过的代理ip中间件注释掉了,加入了crawlera的代理
            # 'scrapy_crawlera.CrawleraMiddleware': 600
        },
        # 为了使crawlera生效,需求添加你创建的api信息(如果填写了API key的话,pass可以设置为空)
        # 'CRAWLERA_ENABLED': True,
        # # 'CRAWLERA_USER'="<API KEY>"
        # 'CRAWLERA_USER': "d29317ce66ec428794826a03eb6623e3",
        # 'CRAWLERA_PASS': '',

        'CONCURRENT_REQUESTS': 32,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,

        'AUTOTHROTTLE_ENABLED': False,

        'DOWNLOAD_TIMEOUT': 600,
    }
    def parse(self, response):
        house_list=response.xpath('//div[@id="list-content"]/div')[1:]

        for div in house_list:
            item=AnJuKezfItem()
            item['title']=div.xpath('./div[1]/h3/a/text()').extract_first()
            item['room_mode']=div.xpath('normalize-space(./div[1]/p[1]/text())').extract_first()

            item['house_sq']=div.xpath("./div[1]/p[1]/text()[2]").extract_first()
            item['floor']=div.xpath("./div[1]/p[1]/text()[3]").extract_first()
            item['RA_name']=div.xpath("normalize-space(./div[1]/p[1]/text()[4])").extract_first()

            item['location']=div.xpath("./div[1]/address/text()").re_first()
            # item['location']=item['location']
            item['house_detail_url']=div.xpath("./a/@href").extract_first()
            item['house_community_url']=div.xpath("./div[1]/address/a/@href").extract_first()

            item['rent_mode']=div.xpath("./div[1]/p[2]/span[1]/text()").extract_first()
            item['direction']=div.xpath("./div[1]/p[2]/span[2]/text()").extract_first()
            item['Subway_traffic']=div.xpath("./div[1]/p[2]/span[3]/text()").extract_first()
            item['price']=div.xpath("./div[@class='zu-side']/p/*/text()").extract_first()


            yield item
        next_url=response.xpath('//div[@class="page-content"]/div/a[7]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                dont_filter=True

        )
