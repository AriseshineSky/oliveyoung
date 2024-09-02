from typing import Any, Iterable
import scrapy
from scrapy.http import HtmlResponse


# python3 -m bettervalue_test.test_spiders.test_product
class BetterValueSpider(scrapy.Spider):
    name = "bettervalue"
    allowed_domains = ['bettervaluepharmacy.com.au']
    start_urls = ['https://bettervaluepharmacy.com.au']

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh;q=0.6",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": "your_cookie_here",
            "Referer": "https://bettervaluepharmacy.com.au/products/ostelin-kids-vitamin-d3-liquid-20ml",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(self.start_urls[0], headers=self.headers, callback=self.parse_categories)

    def parse_cat_products(self, response: HtmlResponse):
        pass

    def parse_categories(self, response: HtmlResponse):
        pass
