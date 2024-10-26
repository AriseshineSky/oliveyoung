from datetime import datetime
import json
import scrapy

from urllib.parse import urlparse, parse_qs

from em_product.resources.base_spider import BaseSpider


class ProductUrlSpider(BaseSpider):
    name = "product-url"
    start_urls = []

    def get_json_data(self, ctgrNo, pageNum, rowsPerPage):
        json_data = {
            "accParam": "",
            "langCode": "en",
            "previewDate": "",
            "encKey": "",
            "encText": "",
            "dlvCntry": "10",
            "mrgnCntryCode": "",
            "ctgrNo": ctgrNo,
            "prdtSortStdrCode": "10",
            "pageNum": pageNum,
            "rowsPerPage": rowsPerPage,
            "attrValNoList": {},
            "brandNoList": [],
            "ctgrNoList": [],
            "eventSlprcDscntRt": [],
            "reviewScore": [],
            "scrollY": 12757.599609375,
            "originMin": 2.92,
            "originMax": 197,
        }
        return json_data

    def get_cookies(self):
        cookies = {
            "acesCntry": "00",
            "dlvCntry": "10",
            "currency": "USD",
            "curLang": "en",
            "lang": "en",
            "_gcl_au": "1.1.1196416096.1729959535",
            "_tt_enable_cookie": "1",
            "_ttp": "cJuDPSfVIbj6tMUxxvrPOUj-28o",
            "_gid": "GA1.2.313340108.1729959536",
            "_scid": "oS0wFQ0H1-KlrZA9eGAuCcky_J_T1NDC",
            "ck_ag_pop": "N",
            "_ScCbts": "%5B%2283%3Bchrome.2%3A2%3A5%22%5D",
            "_sctr": "1%7C1729918800000",
            "FOSID": "YzFlODRjOTQtOWZmMS00NjA3LTlhMzctNzVmOWFkNzA3YWQx",
            "_gat_UA-141211198-1": "1",
            "_scid_r": "sq0wFQ0H1-KlrZA9eGAuCcky_J_T1NDCM1g7QA",
            "_ga": "GA1.1.180517182.1729959535",
            "_ga_5ZDXC4W9LE": "GS1.1.1729969175.2.1.1729969274.55.0.0",
        }
        return cookies

    def get_headers(self, referer):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://global.oliveyoung.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": referer,
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

        return headers

    custom_settings = {
        "ITEM_PIPELINES": {
            "oliveyoung.pipelines.ProductUrlPipeline": 400,
        }
    }

    def start_requests(self):
        for url in ProductUrlSpider.start_urls:
            yield scrapy.Request(
                "https://global.oliveyoung.com/display/category/product-data/",
                method="POST",
                headers=self.get_headers(url),
                cookies=self.get_cookies(),
                meta={"referer": url},
                body=json.dumps(
                    self.get_json_data(self.get_category_no(url), 1, 24)
                ),  # 设置 JSON 数据
                callback=self.parse,
            )

    def get_category_no(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("ctgrNo", [None])[0]

    def get_product_id(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("prdtNo", [None])[0]

    def parse(self, response):
        res = response.json()
        total = res["hits"]["found"]
        start = res["hits"]["start"]
        for hit in res["hits"]["hit"]:
            product_id = hit["fields"]["prdtNo"]
            url = f"https://global.oliveyoung.com/product/detail?prdtNo={product_id}"

            yield {
                "id": product_id,
                "url": url,
                "date": datetime.now().replace(microsecond=0).isoformat(),
            }

        if start + 24 < total:
            yield scrapy.Request(
                "https://global.oliveyoung.com/display/category/product-data/",
                method="POST",
                headers=self.get_headers(response.meta["referer"]),  # 设置请求头
                meta={"referer": response.meta["referer"]},
                cookies=self.get_cookies(),  # 设置 cookies
                body=json.dumps(
                    self.get_json_data(
                        self.get_category_no(response.meta["referer"]),
                        (start) / 24 + 2,
                        24,
                    )
                ),
                callback=self.parse,
            )
