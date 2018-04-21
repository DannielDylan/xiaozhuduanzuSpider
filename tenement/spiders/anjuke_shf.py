# -*- coding: utf-8 -*-
import scrapy
from anaconda_project.requirements_registry.network_util import urlparse
from scrapy.loader import ItemLoader

from tenement.items import AnJuKeSaleItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjukeshf'
    allowed_domains = ['anjuke.com']
    # 城市名拼音
    city_name='hangzhou'
    start_urls = ['https://{}.zu.anjuke.com/sale/'.format(city_name)]
    custom_settings = {
        'ITEM_PIPELINES': {
        'tenement.pipelines.TenementPipeline': 300,},
        'DOWNLOADER_MIDDLEWARES': {
            'tenement.middlewares.TenementSpiderMiddleware': 543,
            'tenement.middlewares.IPProxiesMiddleware': 560,
            'tenement.middlewares.RandomUserAgent': 565,
        }
    }
    def parse(self, response):
        # next_url = response.xpath('//div[@id="content"]/div[4]/div[7]/a[7]/@href').extract()[0]
        next_url = response.xpath('//div[@id="content"]/div[4]/div[7]/a[7]/@href')
        for url in next_url.extract():

            yield scrapy.Request(
                urlparse.urljoin(response.url,url,dont_filter=True)
            )
        # 爬取每一页的链接
        house_num=len(response.xpath('//*[@id="houselist-mod-new"]/li').extract())
        for i in range(1, house_num + 1):
            url = response.xpath('//div[@id="houselist-mod-new"]/li[{}]/div[2]/div[1]/a/@href'
                    .format(i)).extract()[0]
            yield scrapy.Request(url, callback=self.parse_detail)

        # next_url=response.xpath('//div[@id="content"]/div[4]/div[7]/a[7]/@href').extract()[0]
        # print('正在爬取的' + str(next_url))
        # if next_url:
        #     yield scrapy.Request(
        #         url=next_url,
        #         callback=self.parse
        #     )

    def parse_detail(self,response):
        house_info=response.xpath('//div[@class="houseInfo-wrap"]')
        if house_info:
            for div in house_info:

                item=AnJuKeSaleItem()
                item['area']=div.xpath( '//div/div[2]/dl[2]/dd/text()')
                item['mode']=div.xpath( '//div/div[2]/dl[1]/dd/text()')
                item['floor']=div.xpath('//div/div[2]/dl[4]/dd/text()')
                item['age']=div.xpath('//div/div[1]/dl[3]/dd/text()')
                item['price']=div.xpath('//div/div[3]/dl[2]/dd/text()')
                item['location']=div.xpath('//div/div[1]/dl[1]/dd/a/text()')
                item['district']=div.xpath('//div/div[1]/dl[2]/dd/p/a[1]/text()')
                print(item)
                yield item


