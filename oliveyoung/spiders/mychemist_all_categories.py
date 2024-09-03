import sys
sys.path.append(sys.path[0] + '/..')

import scrapy
from scrapy.http import HtmlResponse


# scrapy runspider all_categories.py
class MyChemistAllCategories(scrapy.Spider):
    name = "mychemist_all_categories"
    allowed_domains = ["mychemist.com.au"]
    start_urls = ['https://www.mychemist.com.au/categories']

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
            "Referer": "https://www.mychemist.com.au",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    def parse(self, response: HtmlResponse):
        pass
