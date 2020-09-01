import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse

class BrokenImageChecker(scrapy.Spider):
    name = 'BrokenImageChecker'

    def parse(self, response):

        src = response.css('img:not([src^="#"])')
        src = src.css('img:not([src^="{"])')
        src = src.css('img:not([src^="/"])')
        src = src.css('img:not([src=""])::attr(src)').extract()

        src = set(src)

    @staticmethod
    def work():
        process = CrawlerProcess()

        start_urls = ['https://scrapy.org/']

        process.crawl(BrokenImageChecker,start_urls=start_urls)
        process.start()
