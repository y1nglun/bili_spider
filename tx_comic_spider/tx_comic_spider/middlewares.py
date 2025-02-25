# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.python import global_object_name
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TxComicSpiderSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TxComicSpiderDownloaderMiddleware:
    def process_request(self, request, spider):
        delay = random.uniform(0.5, 1.5)  # 设置延迟范围，可以根据需要进行调整
        request.meta['delay'] = delay

    def process_response(self, request, response, spider):
        if 'delay' in request.meta:
            delay = request.meta['delay']
            time.sleep(delay)  # 等待延迟时间
            del request.meta['delay']
        return response

    def process_exception(self, request, exception, spider):
        if 'delay' in request.meta:
            delay = request.meta['delay']
            time.sleep(delay)  # 等待延迟时间
            del request.meta['delay']
        return None
