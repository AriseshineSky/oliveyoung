import asyncio
from datetime import datetime
import html
from re import findall

import scrapy
import json
# from oliveyoung.items import OliveyoungProductItem
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
            self.details = None
            self.feedback = { "reviews": None, "rating": None }
            self.description = { "description": None }

            _ = self.crawl_product(url)

            if isinstance(self.details, dict):
                specs = self.crawl_product_specs(url)
                yield {**self.details, **self.feedback, **self.description, **specs}

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

    def crawl_product_specs(self, url):
        meta = self.get_meta()
        id = self.get_product_id(url)
        link = "https://global.oliveyoung.com/product/description-info"
        body = """{"prdtNo":"%s"}""" % id

        meta["playwright_page_methods"] = [
            PageMethod("route", "**/*", self.intercept_request_with_body(body)),
        ]

        return scrapy.Request(link, meta=meta, callback=self.parse_specifications)

    def crawl_product(self, url):
        return scrapy.Request(url, meta=self.get_meta(), callback=self.parse)

    async def intercept_network_response(self, response):
        """
        （自动）收到网路回答时触发
        """

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

            if vendors and ("product" in vendors):
                product = vendors["product"]
                print(product)
                
                existence = 1 if product['tempOutOfStockYn'] == 'N' else 0
                categories = " > ".join(cat for cat in product['allPathCtgrName'].split(' &gt; ')) if product['allPathCtgrName'] else None

                images = None
                videos = None

                if product["thumbnailList"]:
                    img_list = []
                    vid_list = []

                    for media in product['thumbnailList']:
                        if media['videoYn'] == 'Y':
                            vid_list.append(media["movUrl"])
                        else:
                            img_list.append("https://image.globaloliveyoungshop.com/"+media["imagePath"])

                    if img_list:
                        images = ";".join(img_list)
                    if vid_list:
                        videos = ";".join(vid_list)
                elif product["imagePath"]:
                    images = "https://image.globaloliveyoungshop.com/"+product["imagePath"]

                available_qty = 0 if not existence else None
                options = None
                variants = None

                if product['optionList']:
                    if available_qty is None:
                        available_qty = product['optionList'][0]['buyStockQty'] # 第一个变种即本品

                    options = [{
                        "id": None,
                        "name": "Type"
                    }]

                    variants = []
                    for var in product['optionList']:
                        var_imgs = []
                        if var['optnImagePath']:
                            var_imgs = "https://image.globaloliveyoungshop.com/"+var["optnImagePath"]
                        for i in range(1, 4):
                            if var[f'colrChipImagePath{i}']:
                                var_imgs.append("https://image.globaloliveyoungshop.com/"+var[f"colrChipImagePath{i}"])

                        variants.append({
                            "variant_id": var['prdtNo'],
                            "barcode": var['gdsCd'],
                            "sku": var['prdtNo'],
                            "option_values": [{
                                "name": "Type",
                                "value": var['snglOptnName']
                            }],
                            "images": ";".join(var_imgs) if var_imgs else None,
                            "price": var['saleAmt'],
                            "available_qty": var['buyStockQty']
                        })

                # if not product["brandName"]:
                #     brand = ""
                # else:
                #     brand = product["brandName"]

                # title = product["prdtName"]
                # categories = " > ".join(
                #     html.unescape(product["allPathCtgrName"]).split(">")[1:]
                # )
                # if product["optionList"]:
                #     for variant in product["optionList"]:
                #         sku = (
                #             "oliveyoung"
                #             + "_"
                #             + str(variant["prdtNo"])
                #             + "_"
                #             + str(variant["gdsCd"])
                #         )
                #         if "gdsCd" in product:
                #             upc = variant["gdsCd"]
                #         else:
                #             upc = ""
                #         if variant["snglOptnName"]:
                #             ntitle = title + " - " + variant["snglOptnName"]
                #         else:
                #             ntitle = title
                #         ltitle = product["korPrdtName"]
                #         price = variant["saleAmt"]
                #         if variant["tempOutOfStockYn"] == "N":
                #             stock = True
                #         else:
                #             stock = False
                #         nimages = []
                #         if variant["colrChipImagePath1"]:
                #             nimages.append(
                #                 "https://image.globaloliveyoungshop.com/"
                #                 + variant["colrChipImagePath1"]
                #             )
                #         if variant["colrChipImagePath2"]:
                #             nimages.append(
                #                 "https://image.globaloliveyoungshop.com/"
                #                 + variant["colrChipImagePath2"]
                #             )
                #         if variant["colrChipImagePath3"]:
                #             nimages.append(
                #                 "https://image.globaloliveyoungshop.com/"
                #                 + variant["colrChipImagePath3"]
                #             )
                #         if variant["optnImagePath"]:
                #             nimages.append(
                #                 "https://image.globaloliveyoungshop.com/"
                #                 + variant["optnImagePath"]
                #             )

                #         if nimages:
                #             nimages = nimages + images
                #             image = nimages[0]
                #         else:
                #             nimages = images
                #             image = images[0]

                        # breakpoint()
                        # item = {
                        #     "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                        #     "url": f"https://global.oliveyoung.com/product/detail?prdtNo={product['prdtNo']}",
                        #     "source": "OLIVE YOUNG",
                        #     "product_id": sku,
                        #     "title": ltitle,
                        #     "title_en": ntitle,
                        #     "sku": sku,
                        #     "categories": categories,
                        #     "brand": brand,
                        #     "source": "oliveyoung",
                        #     "images": nimages,
                        #     "price": price,
                        #     "available_qty": stock * 3,
                        #     "upc": upc,
                        # }
                        # yield item
                self.details = {
                    "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    "url": f"https://global.oliveyoung.com/product/detail?prdtNo={product['prdtNo']}",
                    "source": "OLIVE YOUNG",
                    "product_id": product['prdtNo'],
                    "existence": existence,
                    "title": product['korPrdtName'],
                    "title_en": product['prdtName'],
                    "summary": None,
                    "sku": product['prdtNo'],
                    "upc": product['gdsCd'],
                    "brand": product['brandName'],
                    "categories": categories,
                    "images": images,
                    "videos": videos,
                    "price": product['saleAmt'],
                    "available_qty": available_qty,
                    "options": options,
                    "variants": variants,
                    "returnable": 0,
                    "sold_count": None,
                    "shipping_fee": 0.00 if product['saleAmt'] >= 60.00 else None,
                    "shipping_days_min": 5, # https://global.oliveyoung.com/foot-info/footer-contents?foterMenuSeq=10
                    "shipping_days_max": 7,
                    "width": None,
                    "height": None,
                    "length": None,
                }
        elif 'product/review-summary' in response.url:
            breakpoint()
            try:
                content = await response.text()
                summary = json.loads(content)
            except json.decoder.JSONDecodeError:
                content = ""
                summary = None

            if summary and ('totalReviewCount' in summary) and ('totalStarRate' in summary):
                self.feedback['reviews'] = summary['totalReviewCount']
                self.feedback['rating'] = round(float(summary['totalStarRate']), 1)
        elif 'product/details-info' in response.url:
            breakpoint()
            try:
                content = await response.text()
                info = json.loads(content)
            except json.decoder.JSONDecodeError:
                content = ""
                info = None
        
            if info and ('details' in info):
                details = info['details']
                descr = ""
                
                if details['sellingPointText'] or details['whyWeLoveItText'] or details['ftrdIngrdText'] or details['howToUseText']:
                    descr += '<div class="oliveyoung-descr">'
                    descr += '  <h2>Product infos</h2>\n'
                    if details['sellingPointText']:
                        descr += '  <h3>Selling point</h3>\n'
                        descr += f'  <div>{details['sellingPointText']}</div>'
                    if details['whyWeLoveItText']:
                        descr += '  <h3>Why we love it</h3>\n'
                        descr += f'  <div>{details['whyWeLoveItText']}</div>'
                    if details['ftrdIngrdText']:
                        descr += '  <h3>Featured ingredients</h3>\n'
                        descr += f'  <div>{details['ftrdIngrdText']}</div>'
                    if details['howToUseText']:
                        descr += '  <h3>How to use</h3>\n'
                        descr += f'  <div>{details['howToUseText']}</div>'
                    descr += '</div>\n'

                # TODO：解析图片

                self.description['description'] = descr

    def intercept_request_with_body(self, body):
        """
        （手动）发出请求时触发
        """

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

    def parse_specifications(self, response):
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
            weight = None

            if "description" in data:
                for detail in data["description"]:
                    key = detail["codeDtlName"]
                    if "Customer Service" not in key and "itemCont" in detail:
                        value = detail["itemCont"]
                        specifications.append({"key": key, "value": value})
                    if "weight" in key:
                        wm = findall(r"([\d\.]+)\s*([A-Za-z]+)", value)
                        if wm:
                            amount = float(wm[0][0])
                            unit = wm[0][1].lower()

                            if (unit == 'kg') or (unit == 'l'):
                                weight = round(amount*2.204623, 2)
                            elif (unit == 'g') or (unit == 'ml'):
                                weight = round(amount*0.002205, 2)
            
            breakpoint()
            item = {
                "specifications": specifications,
                "weight": weight,
            }

            self.log(f"Item: {item}")
            return item
        else:
            return {
                "specifications": None,
                "weight": None
            }

    def parse(self, response):
        page = response.meta["playwright_page"]
        page.on(
            "response",
            lambda response: asyncio.ensure_future(
                self.intercept_network_response(response)
            ),
        )
