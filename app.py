import crochet

from database_connect import connect_to_db
from urls import Urls

crochet.setup()

from flask import Flask, render_template
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from SpiderBot.spiders import spider
from flask_restful import reqparse


search_index_parser = reqparse.RequestParser()
search_index_parser.add_argument('search', type=str, required=False)

app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()


@app.route("/")
def send_request():
    args = search_index_parser.parse_args()
    search_string = args.search
    if search_string is None or not search_string:
        return render_template('index.html')
    else:
        all_links = scrape(search_string, Urls.urls)
        return render_template('result_page.html', indices=all_links)


def scrape(search_string, given_links):
    urls = given_links.copy()
    all_links = []
    found_urls = []
    global output_data
    output_data = []

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
                found_urls.append(result[0])
                words = result[2].replace('.', ' ').replace("\"", ' ').split()
                url_client.update_one({'url': result[0]}, {'$set': {'title': result[1]}}, upsert=True)
                for word in words:
                    if word_client.find_one({word: {'$exists': True}}) and not word_client.find_one({word: result[0]}):
                        word_client.update_one({word: {'$exists': True}}, {'$push': {word: result[0]}}, upsert=True)
                    else:
                        word_client.insert_one({word: [result[0]]})
            except:
                continue
        except:
            break

    if found_urls:
        for split_words in search_string.split():
            regex_search = '/*%s/*' % split_words
            found_match = list(word_client.aggregate([
                {"$addFields": {
                    "finder": {"$objectToArray": "$$ROOT"}
                }},
                    {"$match": {"finder.k": {'$regex': regex_search, '$options': 'i'}}}
                ]))
            if found_match:
                for all_matching_words in found_match:
                    for matching_url in all_matching_words.get('finder')[1].get('v'):
                        match = False
                        if len(all_links) != 0:
                            for link in all_links:
                                if matching_url == link.get('url'):
                                    match = True
                                    break
                        if match:
                            break
                        unique_info = {}
                        get_link_info = url_client.find_one({'url': matching_url})
                        unique_info['url'] = get_link_info.get('url')
                        unique_info['title'] = get_link_info.get('title')
                        all_links.append(unique_info)
    return all_links



@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(urls):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(spider.SpiderSpider,  searchUrl=urls)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__=='__main__':
    app.run('0.0.0.0', 8080, debug=True)