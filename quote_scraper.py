import scrapy


class QuoteSpider(scrapy.Spider):

    name = 'quote'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]

    def parse(self, response):
        text = response.xpath('//body//text()').getall()
        actual_words = []
        for entry in text:
            if '\n' in entry:
                continue
            actual_words.append(entry)
        if not actual_words:
            yield

        resp = ''.join(actual_words)
        self.quotes_list.append(resp)
        self.link_list.append(response.request.url)


