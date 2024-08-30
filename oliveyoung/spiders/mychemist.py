from datetime import datetime
from re import findall
import scrapy
from scrapy.http import HtmlResponse

class MyChemistSpider(scrapy.Spider):
    name = "mychemist"
    allowed_domains = ['mychemist.com.au']
    start_urls = []
    
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
            "Referer": "https://www.mychemist.com.au/buy/87343/ki-cold-and-flu-day-night-30-tablets",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    def get_product_id(self, url: str):
        id_match = findall(r'buy/(\d+)', url)
        if id_match:
            return id_match[0]

    def parse(self, response: HtmlResponse):
        url = response.css('link[rel="canonical"]::attr(href)').get().strip()
        title = response.css('div.presc_skuname div').get().strip()

        # TODO
        description = None

        yield {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "url": url,
            "source": "My Chemist",
            "product_id": self.get_product_id(url),
            "existence": 1,
            "title": title,
            "title_en": title,
            "description": description,
            "summary": None,
            "sku": response.css('div.product-id').get().split(':')[1].strip(),
            "upc": None,
            
        }
