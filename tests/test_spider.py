from app import scrape
from urls import Urls
import unittest


class TestSpider(unittest.TestCase):

    # general test
    def tests_all_urls(self):
        urls = Urls.urls.copy()
        result = scrape('a', Urls.urls)
        self.assertEqual(len(result[0]), len(urls))
        for entry in result[0]:
            self.assertTrue(entry.get('url') in urls)

    # this is to test case sensitivity
    def test_search_string_return_correct_answer_lowercase(self):
        url = 'http://quotes.toscrape.com/page/2/'
        result = scrape('bob', [url])
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].get('url'), url)

    def test_search_string_return_correct_answer_uppercase(self):
        url = 'http://quotes.toscrape.com/page/2/'
        result = scrape('BOB', [url])
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].get('url'), url)

    # this is to make sure that both words are searched for
    def test_every_word_searched_for_gets_accounted_for(self):
        urls = ['http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/1/']
        result = scrape('BOB albert', urls.copy())
        self.assertEqual(len(result[0]), 2)
        for entry in result[0]:
            self.assertTrue(entry.get('url') in urls)

    # this is to make whole words are not needed to be searched on
    def test_a_whole_word_is_not_needed_to_match(self):
        urls = ['http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/1/']
        result = scrape('indifference', urls.copy())
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0].get('url'), 'http://quotes.toscrape.com/page/2/')

    def test_to_ensure_relevant_ads_appear_when_ads_available(self):
        urls = ['http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/1/']
        result = scrape('football', urls.copy())
        self.assertEqual(result[1].get('zone_id'), 'zone669165852')

    def test_to_ensure_relevant_ads_appear_when_no_ads_available(self):
        urls = ['http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/1/']
        result = scrape('random', urls.copy())
        self.assertEqual(result[1].get('zone_id'), 'zone755505698')
