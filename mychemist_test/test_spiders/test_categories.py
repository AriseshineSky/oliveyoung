import unittest
from scrapy.utils.test import get_crawler
from scrapy.http import HtmlResponse
from oliveyoung.spiders.mychemist import MyChemistSpider


class TestCategories(unittest.TestCase):
    def setUp(self):
        self.crawler = get_crawler(MyChemistSpider)
        self.spider = self.crawler._create_spider()
    
    def test_all_categories(self):
        assert isinstance(self.spider, MyChemistSpider)
        url = "https://www.mychemist.com.au/categories"
        body = None
        with open(
            "mychemist_test/pages/all_categories.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )

        result = list(self.spider.parse_categories(response))
        self.assertEqual(len(result), 2055)

    def test_category_products_v1(self):
        assert isinstance(self.spider, MyChemistSpider)
        url = "https://www.mychemist.com.au/shop-online/6207/nature-s-own-effervescent?size=120"
        body = None
        with open(
            "mychemist_test/pages/category_6207.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse_cat_products(response))
        self.assertEqual(len(result), 8)

    def test_category_products_v2(self):
        assert isinstance(self.spider, MyChemistSpider)
        url = "https://www.mychemist.com.au/shop-online/731/travel-medicine-tma-b2b-products-only?size=120"
        body = None
        with open(
            "mychemist_test/pages/category_731.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse_cat_products(response))
        self.assertEqual(len(result), 573)


if __name__ == '__main__':
    unittest.main()
