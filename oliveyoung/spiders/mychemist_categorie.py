import sys
sys.path.append(sys.path[0] + '/..')

import scrapy
from scrapy.http import HtmlResponse


# scrapy crawl mychemist_categorie -O mychemist_produit_links.json
class MyChemistCategorie(scrapy.Spider):
    name = "mychemist_categorie"
    allowed_domains = ["mychemist.com.au"]
    start_urls = [
        'https://www.mychemist.com.au/shop-online/6207/nature-s-own-effervescent?size=120',
        'https://www.mychemist.com.au/shop-online/731/travel-medicine-tma-b2b-products-only?size=120'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            "Referer": "https://www.mychemist.com.au/categories",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
    
    def start_requests(self):
        for su in self.start_urls:
            yield scrapy.Request(su, headers=self.headers, callback=self.parse)

    def parse(self, response: HtmlResponse):
        try:
            total_pages = response.meta.get('total_pages')
            actual_page = response.meta.get('actual_page')
        except:
            total_pages = None
            actual_page = None

        if total_pages is None:
            total_pages = 1
            actual_page = 1
            total_sel = response.css('div.pager-count')
            if total_sel:
                total_pages = -(int(total_sel.css('::text').get().strip().split()[0]) // -120)

        links = ['https://www.mychemist.com.au'+a.css('::attr(href)').get() for a in response.css('a.product-container')]
        for l in links:
            yield {
                "categorie_link": response.url,
                "product_link": l
            }
        
        if actual_page < total_pages:
            next_link = 'https://www.mychemist.com.au'+response.css('a.next-page::attr(href)').get()
            yield scrapy.Request(next_link, headers=self.headers, meta={
                'total_pages': total_pages,
                'actual_page': actual_page+1
            })
