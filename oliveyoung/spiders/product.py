from datetime import datetime
from re import findall

import scrapy
import json


from urllib.parse import urlparse, parse_qs


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["oliveyoung.com"]
    start_urls = []

    custom_settings = {
        "ITEM_PIPELINES": {
            "oliveyoung.pipelines.ProductPipeline": 400,
        }
    }

    def get_product_id(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("prdtNo", [None])[0]

    def get_json_data(self, prdtNo):
        json_data = {
            "prdtNo": prdtNo,
        }
        return json_data

    def get_headers(self, referer):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json",
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
            "_ga": "GA1.2.180517182.1729959535",
            "_scid_r": "xq0wFQ0H1-KlrZA9eGAuCcky_J_T1NDCM1g7RA",
            "_ga_5ZDXC4W9LE": "GS1.1.1729969175.2.1.1729971618.60.0.0",
            "_dd_s": "rum=0&expire=1729972519259",
        }
        return cookies

    def start_requests(self):
        for url in ProductSpider.start_urls:
            yield scrapy.Request(
                "https://global.oliveyoung.com/product/detail-data",
                method="POST",
                headers=self.get_headers(url),
                meta={"referer": url},
                cookies=self.get_cookies(),
                body=json.dumps(self.get_json_data(self.get_product_id(url))),
            )

    def get_existence(self, product_info):
        return True if product_info["tempOutOfStockYn"] == "N" else False

    def get_categories(self, product_info):
        return (
            " > ".join(cat for cat in product_info["allPathCtgrName"].split(" &gt; "))
            if product_info["allPathCtgrName"]
            else None
        )

    def parse_specifications(self, response):
        product = response.meta["product"]
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

                        if (unit == "kg") or (unit == "l"):
                            weight = round(amount * 2.204623, 2)
                        elif (unit == "g") or (unit == "ml"):
                            weight = round(amount * 0.002205, 2)

        if specifications:
            product["specifications"] = (specifications,)

        if weight:
            product["weight"] = (weight,)
        yield product

    def get_images(self, product_info):
        if "thumbnails" in product_info:
            return ";".join(
                [
                    f"https://image.globaloliveyoungshop.com/{thumbnail['imagePath']}"
                    for thumbnail in product_info["thumbnails"]
                ]
            )
        elif "imagePath" in product_info:
            return "https://image.globaloliveyoungshop.com/" + product_info["imagePath"]
        else:
            return None

    def parse(self, response):
        res = response.json()
        product_info = res["product"]
        key_maps = {
            "product_id": "prdtNo",
            "title": "korPrdtName",
            "title_en": "prdtName",
            "available_qty": "buyStockQty",
            "sku": "prdtNo",
            "brand": "brandName",
            "price": "saleAmt",
            "upc": "gdsCd",
        }

        product = {
            "shipping_days_min": None,
            "shipping_days_max": None,
            "date": datetime.now().replace(microsecond=0).isoformat(),
            "url": response.url,
            "reviews": None,
            "rating": None,
            "shipping_fee": 0,
            "width": None,
            "height": None,
            "length": None,
            "sold_count": None,
            "source": "Oliveyoung",
            "summary": None,
        }
        for key, value in key_maps.items():
            product[key] = product_info.get(value)

        product["images"] = self.get_images(product_info)

        product["existence"] = self.get_existence(product_info)
        product["categories"] = self.get_categories(product_info)

        if product["optionList"]:
            if product["available_qty"] is None:
                product["available_qty"] = product["optionList"][0]["buyStockQty"]

            options = [{"id": None, "name": "Composition"}]

            variants = []
            for var in product["optionList"]:
                var_imgs = []
                if var["optnImagePath"]:
                    var_imgs = (
                        "https://image.globaloliveyoungshop.com/" + var["optnImagePath"]
                    )
                for i in range(1, 4):
                    if var[f"colrChipImagePath{i}"]:
                        var_imgs.append(
                            "https://image.globaloliveyoungshop.com/"
                            + var[f"colrChipImagePath{i}"]
                        )

                variants.append(
                    {
                        "variant_id": var["prdtNo"],
                        "barcode": var["gdsCd"],
                        "sku": var["prdtNo"],
                        "option_values": [
                            {"name": "Composition", "value": var["snglOptnName"]}
                        ],
                        "images": ";".join(var_imgs) if var_imgs else None,
                        "price": var["saleAmt"],
                        "available_qty": var["buyStockQty"],
                    }
                )

            product["options"] = options
            product["variants"] = variants

        yield scrapy.Request(
            "https://global.oliveyoung.com/product/details-info",
            method="POST",
            headers=self.get_headers(response.meta["referer"]),
            meta={"referer": response.meta["referer"], "product": product},
            cookies=self.get_cookies(),
            body=json.dumps(self.get_json_data(product["product_id"])),
            callback=self.parse_description,
        )

    def parse_description(self, response):
        product = response.meta["product"]
        info = response.json()

        descr = ""
        if info and ("details" in info):
            details = info["details"]

            if (
                details["sellingPointText"]
                or details["whyWeLoveItText"]
                or details["ftrdIngrdText"]
                or details["howToUseText"]
                or details["dtlAddDesc"]
            ):
                descr += '<div class="oliveyoung-descr">\n'
                descr += "  <h2>Product infos</h2>\n"
                if details["sellingPointText"]:
                    descr += "<h3>Selling point</h3>\n"
                    descr += f'<div>{details['sellingPointText'].replace('\r\n', '<br>')}</div>\n'
                if details["whyWeLoveItText"]:
                    descr += "<h3>Why we love it</h3>\n"
                    descr += f'<div>{details['whyWeLoveItText'].replace('\r\n', '<br>')}</div>\n'
                if details["ftrdIngrdText"]:
                    descr += "<h3>Featured ingredients</h3>\n"
                    descr += f'<div>{details['ftrdIngrdText'].replace('\r\n', '<br>')}</div>\n'
                if details["howToUseText"]:
                    descr += "<h3>How to use</h3>\n"
                    descr += f'<div>{details['howToUseText'].replace('\r\n', '<br>')}</div>\n'
                descr += "</div>\n"

            # TODO：解析图片
            if details["optimDtlDesc"] or details["dtlDesc"] or details["dtlAddDesc"]:
                descr += '<div class="oliveyoung-descr">\n'

                if details["dtlAddDesc"]:
                    descr += f'  <div>{details['dtlAddDesc'].replace('\r\n', '<br>')}</div>\n'

                if details["optimDtlDesc"]:
                    img_match = findall(
                        r"data-src\s*=\s*&quot;([^\s]*)&quot;",
                        details["optimDtlDesc"],
                    )
                    if img_match:
                        for m in img_match:
                            descr += f'    <img src="https:{m}">\n'
                elif details["dtlDesc"]:
                    img_match = findall(
                        r"src\s*=\s*&quot;([^\s]*)&quot;", details["dtlDesc"]
                    )
                    if img_match:
                        for m in img_match:
                            descr += f'    <img src="{m}">\n'

                descr += "</div>\n"

        product["description"] = descr

        yield scrapy.Request(
            "https://global.oliveyoung.com/product/description-info",
            method="POST",
            headers=self.get_headers(response.meta["referer"]),
            meta={"referer": response.meta["referer"], "product": product},
            cookies=self.get_cookies(),
            body=json.dumps(self.get_json_data(product["product_id"])),
            callback=self.parse_specifications,
        )
