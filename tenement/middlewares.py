# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random, base64

# from proxies import get_proxy
from proxy_ip import Proxies
import time

import requests


# 付费代理阿布云:
# url = 'http://httpbin.org/get'
#
# # 代理服务器
# proxy_host = 'proxy.abuyun.com'
# proxy_port = '9020'
#
# # 代理隧道验证信息
# proxy_user = '.....'
# proxy_pass = '.....'
#
# proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
#     'host': proxy_host,
#     'port': proxy_port,
#     'user': proxy_user,
#     'pass': proxy_pass,
# }
# proxies = {
#     'http': proxy_meta,
#     'https': proxy_meta,
# }
# response = requests.get(url, proxies=proxies)
# print(response.status_code)
# print(response.text)
from scrapy import signals

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
    "Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) "
    "Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) "
    "Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) "
    "Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
    "Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
    "Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) "
    "Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
    "Chrome/19.0.1055.1 Safari/535.24"
]


class TenementSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IPProxiesMiddleware(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # def get_random_proxy(self):
    #     while 1:
    #         with open(r"proxies.txt", 'r') as f:
    #             proxies = f.readlines()
    #             if proxies:
    #                 break
    #             else:
    #                 time.sleep(1)
    #     proxy = random.choice(proxies).strip()
    #     return proxy

    def process_request(self, request, spider):
        # proxy = self.get_random_proxy()
        proxies=[
            'http://177.72.56.155:3128',
            'http://185.88.255.2:8080',
            'http://103.210.56.38:8082',
            'http://106.14.9.131:9000',
            'http://212.41.231.213:3128'

        ]
        # proxy=get_proxy()

        proxy = random.choice(proxies)
        print('选出的代理是:%s'%(proxy))
        request.meta['proxy'] =proxy


    # def process_response(self,request,response):
    #     """
    #     如果返回的response状态不是200,就重新生成当前的request对象
    #     :param request:
    #     :param response:
    #     :return:
    #     """
    #     if response.status!=200:
    #         proxy=self.get_random_proxy()
    #         print('this is response ip:'+proxy)
    #         request.meta['[proxy']=proxy
    #         return request
    #     return response


# '''
# 这里用的是免费代理,不用用户名和密码,如果有用户名和密码还要加入以下代码
# proxy_user_pass="USERNAME:PASSWORD"
# encode_user_pass=base64.encodestring(proxy_user_pass)
# request.headers['Proxy-Authorization']='Basic'+encode_user_pass
# '''


class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers['User-Agent'] = useragent
