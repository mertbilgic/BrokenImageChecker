from urllib.parse import urlparse
from datetime import datetime

from scrapy import Request,Spider
from scrapyscript import Job, Processor

from helpers.mongo_helper import crawl_links

class BrokenImageChecker(Spider):
    name = 'BrokenImageChecker'
    result = []

    def start_requests(self):
        yield Request(self.url)

    def parse(self, response):

        src = response.css('img:not([src^="#"])')
        src = src.css('img:not([src^="{"])')
        src = src.css('img:not([src^="/"])')
        src = src.css('img:not([src=""])::attr(src)').extract()

        src = set(src)
        self.update_crawl_urls(src,self.result)
        crawl_links.insert_many(self.result)
        return self.result

    def update_crawl_urls(self,src,result):
        for s in src:
            result.append({
                "group_id":self.g_id,
                "src": s,
                "date":(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            })
        
    @staticmethod
    def work(url,g_id):
        broker_job = Job(BrokenImageChecker, url=url,g_id=g_id)
        processor = Processor(settings=None)
        result = processor.run([broker_job]) 
        return result
        
