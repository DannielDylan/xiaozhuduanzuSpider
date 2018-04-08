# -*- coding: utf-8 -*-
import re
import time

import scrapy
import scrapy_crawlera

from tenement.items import TenementItem


class ShortRentForPigletsSpider(scrapy.Spider):
    name = 'xiaozhu'
    allowed_domains = ['http://xiaozhu.com']
    # start_urls = ['http://%s.xiaozhu.com/'%(name)]
    start_urls = ['http://sh.xiaozhu.com/search-duanzufang-p1-0/']

    # def parse_url(self):
    #     """
    #     sh代表上海...想要看其他城市的房源就直接写对应的城市名称简写
    #     :return:
    #     """
    #     name=input("请输入城市名称的缩写拼音:")
    #     url='http://%s.xiaozhu.com/'%(name)
    #     for a in range(0,14):
    #         start_urls=url+"/search-duanzufang-p{}-0/".format(a)
    #         print(start_urls)
    #         yield Request(start_urls,callback=self.parse)

    # 自定义配置
    custom_settings = {
        'ITEM_PIPELINES': {
            'tenement.pipelines.TenementPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'tenement.middlewares.TenementSpiderMiddleware': 543,
            # 'tenement.middlewares.IPProxiesMiddleware': 300,
            'tenement.middlewares.RandomUserAgent': 400,
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

        'LOG_ENABLED': True,  # 启用logging
        'LOG_ENCODING': 'utf-8',  # 启用logging使用的编码
        'LOG_FILE': 'xiaozhu_%s.log' % time.strftime("%Y%m%d", time.localtime()),  # 在当前目录里创建logging输出文件的文件名
        'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
        # 'LOG_LEVEL': 'DEBUG', 设置log级别
        # 'LOG_LEVEL': 'INFO',
        'LOG_STDOUT': True,

    }

    def parse(self, response):
        print('-' * 100)
        print(response)

        infos = response.xpath('//div[@id="page_list"]/ul/li')
        for li in infos:
            item = TenementItem()
            item['title'] = li.xpath('./div[2]/div/a/span/text()').extract_first()
            item['price'] = li.xpath('./div[2]/span[1]/i/text()').extract_first()
            item['desc'] = li.xpath('./div[2]/div/em/text()').extract_first().strip()
            item['address'] = li.xpath('./a/@href').extract_first()
            item['images'] = li.xpath('./a/img/@lazy_src').extract_first()

            item['superior_products'] = li.select('./div[2]/div/p/span[@class="youpin_ico"]/@title').extract()
            item['superior_products'] = item['superior_products'][0] if len(item['superior_products']) > 0 else None
            item['BTC'] = li.select('./div[2]/div/p/span[@class="shanglv_ico"]/@title').extract()
            item['BTC'] = item['BTC'][0] if len(item['BTC']) > 0 else None
            item['book'] = li.select('./div[2]/div/p/span[@class="suding_ico"]/@title').extract()
            item['book'] = item['book'][0] if len(item['book']) > 0 else None
            item['Resident'] = li.select('./div[2]/div/p/span[@class="changzu_ico"]/@title').extract()
            item['Resident'] = item['Resident'][0] if len(item['Resident']) > 0 else None
            item['free_deposit'] = li.select('./div[2]/div/p/span[@class="mianyajin_ico"]/@title').extract()
            item['free_deposit'] = item['free_deposit'][0] if len(item['free_deposit']) > 0 else None
            item['validate'] = li.select('./div[2]/div/p/span[@class="yanzhen_ico"]/@title').extract()
            item['validate'] = item['validate'][0] if len(item['validate']) > 0 else None
            item['shipai'] = li.select('./div[2]/div/p/span/@title').extract()
            item['shipai'] = item['shipai'][0] if len(item['shipai']) > 0 else None
            item['lock'] = li.select('./div[2]/div/p/span[@class="meisuo_ico"]/@title').extract()
            item['lock'] = item['lock'][0] if len(item['lock']) > 0 else None
            yield item
        next_url = response.xpath('//div[@id="page_list"]/div[1]/a[5]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse, dont_filter=True
            )

