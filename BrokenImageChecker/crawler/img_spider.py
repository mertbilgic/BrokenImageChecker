import scrapy
from scrapy import Request,Spider
from scrapy.crawler import CrawlerProcess,install_reactor
from urllib.parse import urlparse
from datetime import datetime
from helpers.mongo_helper import crawl_links
from scrapyscript import Job, Processor


class BrokenImageChecker(scrapy.Spider):
    name = 'BrokenImageChecker'
    guid="asdasd"

    def start_requests(self):
        yield Request(self.url)

    def parse(self, response):

        src = response.css('img:not([src^="#"])')
        src = src.css('img:not([src^="{"])')
        src = src.css('img:not([src^="/"])')
        src = src.css('img:not([src=""])::attr(src)').extract()

        src = set(src)
        self.write_db(src)

    def write_db(self,src):
        for s in src:
            link={
                "group_id":self.guid,
                "src": s,
                "date":(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            }
            crawl_links.insert_one(link)    
        
    @staticmethod
    def work(url):
        broker_job = Job(BrokenImageChecker, url=url)

        processor = Processor(settings=None)
        processor.run([broker_job]) 
        
