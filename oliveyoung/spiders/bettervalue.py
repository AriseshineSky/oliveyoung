from typing import Any, Iterable
import scrapy
from scrapy.http import HtmlResponse


# python3 -m bettervalue_test.test_spiders.test_product
# python3 -m bettervalue_test.test_spiders.test_categories
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
        prod_ax = response.css('ul#main-collection-product-grid a.card-link')
        links = ['https://bettervaluepharmacy.com.au'+a.css('::attr(href)').get() for a in prod_ax]

        for l in links:
            yield scrapy.Request(l, headers=self.headers,
                                #  callback=
                                 )
        
        if response.css('div.pagination-page-infinite > a.disabled'):
            return
        
        next_url = 'https://bettervaluepharmacy.com.au'+response.css('div.pagination-page-infinite > a::attr(href)').get()
        yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_cat_products)

    def parse_categories(self, response: HtmlResponse):
        cat_ax = response.css('a.header__menu-item')
        cat_lx = [a.css('::attr(href)').get() for a in cat_ax]
        
        cat_filter = set(l for a, l in zip(cat_ax, cat_lx) if a.css('span.icon-dropdown > svg'))
        cat_links = ['https://bettervaluepharmacy.com.au'+l for l in cat_lx
                     if ('/collections/' in l) and (l not in cat_filter)]

        for cl in cat_links:
            yield scrapy.Request(cl, headers=self.headers, callback=self.parse_cat_products)
