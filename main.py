import crochet

from database_connect import connect_to_db

crochet.setup()

from flask import Flask, jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from quotesbot.spiders import spider
from flask_restful import reqparse


search_index_parser = reqparse.RequestParser()
search_index_parser.add_argument('search', type=str, required=False)

app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()


@app.route("/")
def scrape():
    all_links = []
    urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]
    args = search_index_parser.parse_args()
    search_string = args.search
    if search_string is None or not search_string:
        return jsonify(urls)

    found_urls = []

    url_client = connect_to_db('list_of_urls')
    for url in urls:
        check_url = url_client.find_one({'url': url})
        if check_url:
            found_urls.append(check_url.get('url'))
        else:
            url_client.insert_one({'url': url})

    for url in found_urls:
        if url in urls:
            urls.remove(url)
    word_client = connect_to_db('list_of_words')

    # run crawler in twisted reactor synchronously
    scrape_with_crochet(urls)

    for spider_data in output_data:
        result = spider_data.get('resp')
        try:
            try:
                words = result[1].replace('.', ' ').replace("\"", ' ').split()
                for word in words:
                    if word_client.find_one({word: {'$exists': True}}) and not word_client.find_one({word: result[0]}):
                        word_client.update_one({word: {'$exists': True}}, {'$push': {word: result[0]}}, upsert=True)
                    else:
                        word_client.insert_one({word: [result[0]]})
            except:
                continue
            if search_string in result[1]:
                if result[0] not in all_links:
                    all_links.append(result[0])
        except:
            break

    if found_urls:
        found_match = word_client.find_one({search_string: {'$exists': True}})
        if found_match:
            for url in found_match.get(search_string):
                all_links.append(url)
    return jsonify(all_links)


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(urls):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(spider.QuoteSpider,  searchUrl=urls)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__=='__main__':
    app.run('0.0.0.0', 8080, debug=True)