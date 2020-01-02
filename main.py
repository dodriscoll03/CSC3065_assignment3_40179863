import json

from flask import Flask
from scrapy.crawler import CrawlerRunner
from sys import stdout
from twisted.logger import globalLogBeginner, textFileLogObserver
from twisted.web import server, wsgi
from twisted.internet import endpoints, reactor
from quote_scraper import QuoteSpider
from flask_restful import reqparse

search_index_parser = reqparse.RequestParser()
search_index_parser.add_argument('search', type=str, required=False)

app = Flask(__name__)
crawl_runner = CrawlerRunner()
quotes_list = []
link_list = []
scrape_complete = False


@app.route('/')
def crawl_for_quotes():
    # global scrape_complete
    # global quotes_list
    # global link_list
    # quotes_list = []
    # link_list = []
    #
    # args = search_index_parser.parse_args()
    # search_string = args.search
    #
    # # start the crawler and execute a callback when complete
    # eventual = crawl_runner.crawl(QuoteSpider, quotes_list=quotes_list, link_list=link_list)
    # eventual.addCallback(finished_scrape)
    # while not scrape_complete:
    #     continue
    # if not search_string:
    #     return json.dumps(link_list)
    # result = []
    # for index, link in enumerate(link_list):
    #     if search_string in quotes_list[index]:
    #         result.append(link)
    # return json.dumps(result) if result else json.dumps("no result")

    return json.dumps("no result")

def finished_scrape(null):
    global scrape_complete
    scrape_complete = True


if __name__ == '__main__':
    # start the logger
    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 8080)
    http_server.listen(factory)

    # start event loop
    reactor.run()
