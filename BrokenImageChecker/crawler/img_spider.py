from urllib.parse import urlparse
from datetime import datetime

from scrapy import Request,Spider
from scrapyscript import Job, Processor

from helpers.mongo_helper import crawl_links

class BrokenImageChecker(Spider):
    name = 'BrokenImageChecker'

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
                "group_id":self.g_id,
                "src": s,
                "date":(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            }
            crawl_links.insert_one(link)    
        
    @staticmethod
    def work(url,g_id):
        broker_job = Job(BrokenImageChecker, url=url,g_id=g_id)
        processor = Processor(settings=None)
        processor.run([broker_job]) 
        
