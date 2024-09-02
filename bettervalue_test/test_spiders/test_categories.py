import unittest
from scrapy.utils.test import get_crawler
from scrapy.http import HtmlResponse
from oliveyoung.spiders.bettervalue import BetterValueSpider


class TestCategories(unittest.TestCase):
    def setUp(self):
        self.crawler = get_crawler(BetterValueSpider)
        self.spider = self.crawler._create_spider()
    
    def test_all_categories(self):
        assert isinstance(self.spider, BetterValueSpider)
        url = "https://bettervaluepharmacy.com.au/"
        body = None
        with open(
            "bettervalue_test/htmls/index.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse_categories(response))
        self.assertEqual(len(result), 143)

    def test_category_products(self):
        assert isinstance(self.spider, BetterValueSpider)
        url = "https://bettervaluepharmacy.com.au/collections/baby-formula"
        body = None
        with open(
            "bettervalue_test/htmls/coll_babyformula.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse_cat_products(response))
        print(result)
        self.assertEqual(len(result), 182)


if __name__ == '__main__':
    unittest.main()
