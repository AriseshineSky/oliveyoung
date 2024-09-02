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
            "price": 14.27, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": None,
            "width": None,
            "length": None
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
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
            "price": 2.04, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": None,
            "width": None,
            "length": None
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])

    def test_available_product_v3(self):
        url = "https://www.mychemist.com.au/buy/62354/lady-jayne-bobby-pins,-black,-4-5-cm,-pk25"
        body = None
        with open(
            "mychemist_test/pages/p62354_2498326.html",
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
            "url": "https://www.mychemist.com.au/buy/62354/lady-jayne-bobby-pins,-black,-4-5-cm,-pk25",
            "source": "My Chemist",
            "product_id": "62354",
            "existence": True,
            "title": "Lady Jayne Bobby Pins, Black, 4.5 Cm, Pk25",
            "title_en": "Lady Jayne Bobby Pins, Black, 4.5 Cm, Pk25",
            "sku": "2498327",
            "categories": "Personal Care > Hair Care > Lady Jayne > Lady Jayne Accessories",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/62354/2DF_800.jpg;https://static.chemistwarehouse.com.au/ams/media/pi/62354/ADD3_800.jpg",
            "videos": None,
            "price": 2.03, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": None,
            "width": None,
            "length": 1.77
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])
    
    def test_available_product_v4(self):
        url = "https://www.mychemist.com.au/buy/89148/bodifast-tubular-retention-bandage-5cm-x-2m-green"
        body = None
        with open(
            "mychemist_test/pages/p89148_2681025.html",
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
            "url": "https://www.mychemist.com.au/buy/89148/bodifast-tubular-retention-bandage-5cm-x-2m-green",
            "source": "My Chemist",
            "product_id": "89148",
            "existence": True,
            "title": "Bodifast Tubular Retention Bandage 5cm x 2m Green",
            "title_en": "Bodifast Tubular Retention Bandage 5cm x 2m Green",
            "sku": "2681025",
            "categories": "Medicines > First Aid > Bandages and Dressings",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/89148/F2D_800.jpg",
            "videos": None,
            "price": 8.83, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": None,
            "width": 1.97,
            "length": 78.74
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])

    def test_available_product_v5(self):
        url = "https://www.mychemist.com.au/buy/53008/ego-qv-gentle-wash-1-kg"
        body = None
        with open(
            "mychemist_test/pages/p53008_2586306.html",
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
            "url": "https://www.mychemist.com.au/buy/53008/ego-qv-gentle-wash-1-kg",
            "source": "My Chemist",
            "product_id": "53008",
            "existence": True,
            "title": "Ego QV Gentle Wash 1 Kg",
            "title_en": "Ego QV Gentle Wash 1 Kg",
            "sku": "2586306",
            "categories": "Beauty > Skin Care > QV > QV Body",
            "images": "https://static.chemistwarehouse.com.au/ams/media/pi/53008/2DF_800.jpg",
            "videos": None,
            "price": 15.63, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": 2.20,
            "width": None,
            "length": None,
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])
    
    def test_prescription(self):
        url = "https://www.mychemist.com.au/buy/6271/minipress-5mg-tablets-100-prazosin"
        body = None
        with open(
            "mychemist_test/pages/p6271_2489119.html",
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
            "url": "https://www.mychemist.com.au/buy/6271/minipress-5mg-tablets-100-prazosin",
            "source": "My Chemist",
            "product_id": "6271",
            "existence": True,
            "title": "Minipress 5mg Tablets 100 - Prazosin",
            "title_en": "Minipress 5mg Tablets 100 - Prazosin",
            "sku": "2489119",
            "categories": "Prescriptions",
            "images": None,
            "videos": None,
            "price": 11.55, # 澳洲元汇率0.68
            "shipping_days_min": 5,
            "shipping_days_max": 5,
            "weight": None,
            "width": None,
            "length": None
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
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])

    def test_unavailable_product(self):
        url = "https://www.mychemist.com.au/buy/87346/health-beauty-120-cotton-swabs-not-for-sale-in-act"
        body = None
        with open(
            "mychemist_test/pages/p87346.html",
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
            "url": "https://www.mychemist.com.au/buy/87346/health-beauty-120-cotton-swabs-not-for-sale-in-act",
            "source": "My Chemist",
            "product_id": "87346",
            "existence": False,
            "title": "Health & Beauty 120 Cotton Swabs (Not For Sale In ACT)",
            "title_en": "Health & Beauty 120 Cotton Swabs (Not For Sale In ACT)",
            "sku": None,
            "categories": "Clearance > Clearance Beauty Accessories",
            "images": None,
            "videos": None,
            "price": None,
            "available_qty": 0,
            "shipping_days_min": None,
            "shipping_days_max": None,
            "weight": None,
            "width": None,
            "length": None
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
            "available_qty",
            "shipping_days_min",
            "shipping_days_max",
            "weight",
            "width",
            "length"
        ]
        for key in keys:
            self.assertEqual(product[key], target_product[key])


if __name__ == '__main__':
    unittest.main()
