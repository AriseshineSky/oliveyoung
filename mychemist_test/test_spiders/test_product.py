import unittest
from scrapy.utils.test import get_crawler
from scrapy.http import HtmlResponse
from oliveyoung.spiders.mychemist import MyChemistSpider


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.crawler = get_crawler(MyChemistSpider)
        self.spider = self.crawler._create_spider()

    def test_available_product_v1(self):
        url = "https://www.mychemist.com.au/buy/87343/ki-cold-and-flu-day-night-30-tablets"
        body = None
        with open(
            "mychemist_test/pages/p87343_2678621.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse(response))
        self.assertEqual(len(result), 1)
        product = result[0]
        target_product = {
            "url": "https://www.mychemist.com.au/buy/87343/ki-cold-and-flu-day-night-30-tablets",
            "source": "My Chemist",
            "product_id": "87343",
            "existence": True,
            "title": "Ki Cold and Flu Day & Night 30 Tablets",
            "title_en": "Ki Cold and Flu Day & Night 30 Tablets",
            "sku": "2678621",
            "categories": "Medicines > Cold & Flu > Ki Cold & Flu",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/87343/2DF_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/87343/ADD3_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/87343/ADD4_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/87343/ADD5_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/87343/ADD6_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/87343/ADD7_800.jpg",
            "videos": "https://www.youtube.com/embed/umFR29Or5dg",
            "price": 14.27 # 澳洲元汇率0.68
        }

        keys = [
            "url",
            "source",
            "product_id",
            "existence",
            "title",
            "title_en",
            # "description",
            "sku",
            "categories",
            "images",
            "videos",
            "price",
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])
    
    def test_available_product_v2(self):
        url = "https://www.mychemist.com.au/buy/92911/w7-the-full-facial-pore-minimising-2-step-treatment-mask"
        body = None
        with open(
            "mychemist_test/pages/p92911_2680431.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse(response))
        self.assertEqual(len(result), 1)
        product = result[0]
        target_product = {
            "url": "https://www.mychemist.com.au/buy/92911/w7-the-full-facial-pore-minimising-2-step-treatment-mask",
            "source": "My Chemist",
            "product_id": "92911",
            "existence": True,
            "title": "W7 The Full Facial Pore Minimising 2 Step Treatment Mask",
            "title_en": "W7 The Full Facial Pore Minimising 2 Step Treatment Mask",
            "sku": "2680431",
            "categories": "Clearance > Clearance Skincare",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/92911/F2D_800.jpg",
            "videos": None,
            "price": 2.04 # 澳洲元汇率0.68
        }

        keys = [
            "url",
            "source",
            "product_id",
            "existence",
            "title",
            "title_en",
            # "description",
            "sku",
            "categories",
            "images",
            "videos",
            "price",
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])

    def test_available_product_v3(self):
        url = "https://www.mychemist.com.au/buy/92911/w7-the-full-facial-pore-minimising-2-step-treatment-mask"
        body = None
        with open(
            "mychemist_test/pages/p92911_2680431.html",
            "rb",
        ) as file:
            body = file.read()
        response = HtmlResponse(
            url=url,
            body=body,
        )
        result = list(self.spider.parse(response))
        self.assertEqual(len(result), 1)
        product = result[0]
        target_product = {
            "url": "https://www.mychemist.com.au/buy/92911/w7-the-full-facial-pore-minimising-2-step-treatment-mask",
            "source": "My Chemist",
            "product_id": "92911",
            "existence": True,
            "title": "W7 The Full Facial Pore Minimising 2 Step Treatment Mask",
            "title_en": "W7 The Full Facial Pore Minimising 2 Step Treatment Mask",
            "sku": "2680431",
            "categories": "Clearance > Clearance Skincare",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/92911/F2D_800.jpg",
            "videos": None,
            "price": 2.04 # 澳洲元汇率0.68
        }

        keys = [
            "url",
            "source",
            "product_id",
            "existence",
            "title",
            "title_en",
            # "description",
            "sku",
            "categories",
            "images",
            "videos",
            "price",
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])
    
    
