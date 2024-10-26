from datetime import datetime
import scrapy

from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from em_product.resources.base_spider import BaseSpider
import xml.etree.ElementTree as ET


class CategorySpider(BaseSpider):
    name = "category"
    start_urls = ["https://global.oliveyoung.com/sitemapindex-category.xml"]

    def get_cookies(self):
        cookies = {
            "acesCntry": "00",
            "dlvCntry": "10",
            "currency": "USD",
            "curLang": "en",
            "lang": "en",
            "FOSID": "ZmZjOGZmMDMtY2EzNS00NzZkLTlhOGQtNDA5YzZiNjVkNGI4",
            "_gcl_au": "1.1.1196416096.1729959535",
            "_tt_enable_cookie": "1",
            "_ttp": "cJuDPSfVIbj6tMUxxvrPOUj-28o",
            "_gid": "GA1.2.313340108.1729959536",
            "_scid": "oS0wFQ0H1-KlrZA9eGAuCcky_J_T1NDC",
            "ck_ag_pop": "N",
            "_ScCbts": "%5B%2283%3Bchrome.2%3A2%3A5%22%5D",
            "_sctr": "1%7C1729918800000",
            "_ga": "GA1.2.180517182.1729959535",
            "_scid_r": "uq0wFQ0H1-KlrZA9eGAuCcky_J_T1NDCM1g7SA",
            "_ga_5ZDXC4W9LE": "GS1.1.1729959534.1.1.1729959593.1.0.0",
            "_dd_s": "rum=0&expire=1729960509579",
        }
        return cookies

    def get_headers(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        return headers

    custom_settings = {
        "ITEM_PIPELINES": {
            "oliveyoung.pipelines.CategoryPipeline": 400,
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://global.oliveyoung.com/sitemapindex-category.xml",
            method="GET",
            headers=self.get_headers(),
            cookies=self.get_cookies(),
        )

    def get_product_id(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("ctgrNo", [None])[0]

    def parse(self, response):
        root = ET.fromstring(response.text)
        for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if loc is None:
                continue
            url = loc.text
            product_id = self.get_product_id(url)
            if product_id is None:
                continue

            yield {
                "id": product_id,
                "url": url,
                "date": datetime.now().replace(microsecond=0).isoformat(),
            }
