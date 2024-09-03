import sys
sys.path.append(sys.path[0] + '/..')

import scrapy
from scrapy.http import HtmlResponse


# scrapy crawl mychemist_all_categories -O mychemist_categories.json
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
        trx = response.css('div#p_lt_ctl07_pageplaceholder_p_lt_ctl00_wCM_AMS_tg_pnltreeTree table > tr')
        cat_links = ['https://www.mychemist.com.au'+tr.css('td a::attr(href)').get()+'?size=120'
                     for tr in trx if (tr.css('td a') and (not tr.css('td img[alt="Expand"], td img[alt="Collapse"]')))]
        
        for cl in cat_links:
            yield {
                "categorie_link": cl
            }
