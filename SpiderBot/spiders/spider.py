import re

import scrapy


class SpiderSpider(scrapy.Spider):

    name = 'quote'

    def __init__(self, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('searchUrl')

    def parse(self, response):
        all_info = []
        text = response.xpath('//body//text()').getall()
        all_info.append(response.request.url)
        all_info.append(response.css('title::text').get())
        actual_words = []
        for entry in text:
            if '\n' in entry:
                continue
            actual_words.append(entry)
        if not actual_words:
            yield {"resp": all_info}

        resp = ''.join(actual_words)
        all_info.append(resp)
        yield {"resp": all_info}


