import logging
import os

from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor

import scrapy
from scrapy.spiders import CrawlSpider, Rule


class SpiderOne(scrapy.Spider):
    name = "sp1"
    counter = 0
    linkextractor = LinkExtractor(allow=('https://en.wikipedia.org/wiki/(.)'))

    custom_settings = {
        'DEPTH_PRIORITY': '1',
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }



    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_aircraft',
            #"https://en.wikipedia.org/wiki/List_of_aircraft_(0%E2%80%93Ah)",
            #"https://en.wikipedia.org/wiki/List_of_aircraft_(Ai%E2%80%93Am)",
            #'https://en.wikipedia.org/wiki/List_of_aircraft_by_date_and_usage_category',
            #'https://en.wikipedia.org/wiki/List_of_civil_aircraft'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, i=0):
        page = response.url.split("/")[-1]
        filename = f'{self.counter}-{page}.html'

        with open(f"data/{filename}", 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        self.counter += 1



        link = LinkExtractor(allow='https://en.wikipedia.org/wiki/(.)',
                             restrict_css='#mw-content-text > div.mw-parser-output')
        links = link.extract_links(response)
        #print(links)

        #if self.counter == 500:
            #raise CloseSpider('Reached limit 500')

        for _link in links:
            # yield scrapy.Request('http://www.66ip.cn/areaindex_1/1.html', callback=self.parse_list)
            yield scrapy.Request(_link.url, callback=self.parse)
