import asyncio
import html

import scrapy
import json
from oliveyoung.items import OliveyoungProductItem
from scrapy_playwright.page import PageMethod

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["oliveyoung.com"]
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_url_base = "https://global.oliveyoung.com/product/detail?prdtNo="
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
            "Referer": "https://global.oliveyoung.com/product/detail?prdtNo=GA231121180",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    def get_product_id(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("prdtNo", [None])[0]

    def start_requests(self):
        for url in ProductSpider.start_urls:
            yield self.crawl_products(url)
            yield self.crawl_products_description(url)

    def get_meta(self):
        return {
            "playwright": True,
            "playwright_include_page": True,
            "playwright_context_kwargs": {
                "java_script_enabled": True,
                "ignore_https_errors": True,
            },
            "playwright_page_methods": [PageMethod("wait_for_selector", "body")],
        }

    def crawl_products_description(self, url):
        meta = self.get_meta()
        id = self.get_product_id(url)
        link = "https://global.oliveyoung.com/product/description-info"
        body = """{"prdtNo":"%s"}""" % id

        meta["playwright_page_methods"] = [
            PageMethod("route", "**/*", self.intercept_request_with_body(body)),
        ]

        return scrapy.Request(link, meta=meta, callback=self.parse_description)

    def crawl_products(self, url):
        return scrapy.Request(url, meta=self.get_meta(), callback=self.parse)

    async def intercept_network_response(self, response):
        self.logger.debug("Page title: %s", response.url)
        breakpoint()
        if "product/detail-data" in response.url:
            breakpoint()
            try:
                content = await response.text()
                vendors = json.loads(content)
            except json.decoder.JSONDecodeError:
                content = ""
                vendors = None

            if vendors and "product" in vendors:
                countN = len(vendors["product"])
                product = vendors["product"]
                print(product)
                if product["thumbnailList"]:
                    images = [
                        "https://image.globaloliveyoungshop.com/" + img["imagePath"]
                        for img in product["thumbnailList"]
                    ]
                else:
                    images = (
                        "https://image.globaloliveyoungshop.com/" + product["imagePath"]
                    )

                if not product["brandName"]:
                    brand = ""
                else:
                    brand = product["brandName"]

                title = product["prdtName"]
                categories = ">".join(
                    html.unescape(product["allPathCtgrName"]).split(">")[1:]
                )
                if product["optionList"]:
                    for variant in product["optionList"]:
                        sku = (
                            "oliveyoung"
                            + "_"
                            + str(variant["prdtNo"])
                            + "_"
                            + str(variant["gdsCd"])
                        )
                        if "gdsCd" in product:
                            upc = variant["gdsCd"]
                        else:
                            upc = ""
                        if variant["snglOptnName"]:
                            ntitle = title + " - " + variant["snglOptnName"]
                        else:
                            ntitle = title
                        ltitle = product["korPrdtName"]
                        price = variant["saleAmt"]
                        if variant["tempOutOfStockYn"] == "N":
                            stock = True
                        else:
                            stock = False
                        nimages = []
                        if variant["colrChipImagePath1"]:
                            nimages.append(
                                "https://image.globaloliveyoungshop.com/"
                                + variant["colrChipImagePath1"]
                            )
                        if variant["colrChipImagePath2"]:
                            nimages.append(
                                "https://image.globaloliveyoungshop.com/"
                                + variant["colrChipImagePath2"]
                            )
                        if variant["colrChipImagePath3"]:
                            nimages.append(
                                "https://image.globaloliveyoungshop.com/"
                                + variant["colrChipImagePath3"]
                            )
                        if variant["optnImagePath"]:
                            nimages.append(
                                "https://image.globaloliveyoungshop.com/"
                                + variant["optnImagePath"]
                            )

                        if nimages:
                            nimages = nimages + images
                            image = nimages[0]
                        else:
                            nimages = images
                            image = images[0]

                        breakpoint()
                        item = {
                            "_id": sku,
                            "title": ntitle,
                            "ltitle": ltitle,
                            "sku": sku,
                            "categories": categories,
                            "brand": brand,
                            "source": "oliveyoung",
                            "url": "https://global.oliveyoung.com/product/detail?prdtNo=%s"
                            % product["prdtNo"],
                            "images": nimages,
                            "price": price,
                            "available_qty": stock * 3,
                            "upc": upc,
                        }
                        yield item

    def intercept_request_with_body(self, body):
        async def intercept_request(self, request):
            breakpoint()
            """Modify the request before it is sent."""
            if "product/detail" in request.url:
                headers = {
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
                    "Referer": "https://global.oliveyoung.com/product/detail?prdtNo=GA231121180",
                    "Referrer-Policy": "strict-origin-when-cross-origin",
                }
                breakpoint()
                await request.continue_({"postData": body, "headers": headers})
            else:
                await request.continue_()

        return intercept_request

    def parse_description(self, response):
        page = response.meta["playwright_page"]
        page.on(
            "route",
            lambda route: asyncio.create_task(
                self.intercept_request_with_body(route, route.request)
            ),
        )
        """Parse the response."""
        if response.status == 200:
            data = response.json()
            specifications = []

            if "description" in data:
                for detail in data["description"]:
                    key = detail["codeDtlName"]
                    if "Customer Service" not in key and "itemCont" in detail:
                        value = detail["itemCont"]
                        specifications.append({"key": key, "value": value})

            breakpoint()
            item = {
                "specifications": specifications,
            }

            self.log(f"Item: {item}")

    def parse(self, response):
        page = response.meta["playwright_page"]
        page.on(
            "response",
            lambda response: asyncio.ensure_future(
                self.intercept_network_response(response)
            ),
        )
