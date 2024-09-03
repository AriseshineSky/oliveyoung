from typing import Any, Iterable

import scrapy
from scrapy.http import HtmlResponse


# scrapy crawl bettervalue_cat -O bettervalue_prod_links.json
class BetterValueCatSpider(scrapy.Spider):
    name = 'bettervalue_cat'
    allowed_domains = ['bettervaluepharmacy.com.au']
    start_urls = [
        'https://bettervaluepharmacy.com.au/collections/baby-formula'
    ]

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
            "Referer": "https://bettervaluepharmacy.com.au",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
    
    def start_requests(self) -> Iterable[scrapy.Request]:
        for su in self.start_urls:
            yield scrapy.Request(su, headers=self.headers, callback=self.parse)

    def parse(self, response: HtmlResponse):
        prod_ax = response.css('ul#main-collection-product-grid a.card-link')
        links = ['https://bettervaluepharmacy.com.au'+a.css('::attr(href)').get() for a in prod_ax]

        for l in links:
            yield {
                # "categorie_link": response.url,
                "product_link": l
            }
        
        if response.css('div.pagination-page-infinite > a.disabled'):
            return
        
        next_url = 'https://bettervaluepharmacy.com.au'+response.css('div.pagination-page-infinite > a::attr(href)').get()
        yield scrapy.Request(next_url, headers=self.headers)
    