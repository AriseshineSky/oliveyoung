from html import unescape
from re import findall
import sys
sys.path.append(sys.path[0] + '/..')

from datetime import datetime
from typing import Iterable
import scrapy
from scrapy.http import HtmlResponse


# python3 -m mychemist_test.test_spiders.test_product
# python3 -m mychemist_test.test_spiders.test_categories
class MyChemistSpider(scrapy.Spider):
    name = "mychemist"
    allowed_domains = ['mychemist.com.au']
    start_urls = ['https://www.mychemist.com.au/categories']
    prod_ids = set()

    AUD_RATE = 0.68 # 澳洲元汇率
    
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

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(self.start_urls[0], headers=self.headers, callback=self.parse_categories)

    def get_product_id(self, url: str):
        id_match = findall(r'buy/(\d+)', url)
        if id_match:
            return id_match[0]
    
    def get_title(self, text: str):
        title_match = findall(r'Buy\s+(.*)\s+Online at Chemist Warehouse', text)
        if title_match:
            return title_match[0]
    
    def get_dimensions(self, text: str) -> tuple:
        width = None
        length = None

        match1 = findall(r'([\d\.]+)\s*([A-Za-z]*)\s*[Xx]\s*([\d\.]+)\s*([A-Za-z]+)', text)
        match2 = findall(r'([\d\.]+)\s*([A-Za-z]+)', text)

        if match1:
            for m in match1:
                unit2 = m[3].lower()
                unit1 = m[1].lower() if m[1] else unit2

                amount1 = None
                amount2 = None
                if unit1 == 'm':
                    amount1 = round(float(m[0])*39.37008, 2)
                elif unit1 == 'cm':
                    amount1 = round(float(m[0])*0.393701, 2)
                if unit2 == 'm':
                    amount2 = round(float(m[2])*39.37008, 2)
                elif unit2 == 'cm':
                    amount2 = round(float(m[2])*0.393701, 2)

                if (amount1 is not None) and (amount2 is not None):
                    if amount1 >= amount2:
                        length = amount1
                        width = amount2
                    else:
                        length = amount2
                        width = amount1
                    break
        elif match2:
            for m in match2:
                unit = m[1].lower()
                if unit == 'm':
                    length = round(float(m[0])*39.37008, 2)
                elif unit == 'cm':
                    length = round(float(m[0])*0.393701, 2)
                
                if length is not None:
                    break
            
        return (width, length)

    def get_weight(self, text: str):
        weight = None

        match = findall(r'size:\s*(\d+)\s*([A-Za-z]+)', text)
        if match:
            unit = match[0][1].lower()
            if (unit == 'kg') or (unit == 'l'):
                weight = round(float(match[0][0])*2.204623, 2)
            elif (unit == 'g') or (unit == 'ml'):
                weight = round(float(match[0][0])*0.002205, 2)

        return weight

    def parse(self, response: HtmlResponse):
        url = response.css('link[rel="canonical"]::attr(href)').get().strip()
        prod_id = self.get_product_id(url)
        if prod_id in self.prod_ids:
            return

        existence = True
        out_sel = response.css('div[style="margin:auto ; color:red ; font-size:20px ; text-align:left ; font-weight:bold"]::text')
        if out_sel and ('no longer available' in out_sel.get().lower()):
            existence = False
        
        title = self.get_title(unescape(response.css('title').get()))

        description = None
        weight = None
        descr_sels = response.css('section.product-info-section')
        if descr_sels:
            description = '<div class="mychemist-descr">\n'

            for pis in descr_sels:
                if 'hidden' in pis.attrib.get('class', '').split():
                    continue
                
                h2 = pis.css('h2::text').get().strip()
                cont = pis.css('div.details').get()
                description += f'  <h2>{h2}</h2>\n'
                description += f'  <div>{cont}</div>\n'

                px = response.css('section.product-info-section p')
                if px:
                    for p in px:
                        p_txt = p.css('::text').get().strip().lower()
                        if 'size' in p_txt:
                            weight = self.get_weight(p_txt)
                            break

            description += '</div>\n'
        print(description)
        
        sku = None
        sku_sel = response.css('div.product-id::text')
        if sku_sel:
            sku = sku_sel.get().split(':')[1].strip()

        cats_list = [cat.css("::text").get().strip() for cat in response.css('div.breadcrumbs > a')[1:]]
        categories = " > ".join(cats_list)

        images = None
        imgs = response.css('div.sub_images img')
        img0 = response.css('div#slider_pi_container img::attr(src2)')
        if imgs:
            imgs_list = [img.css('::attr(src)').get().strip().replace('_50.jpg', '_800.jpg') for img in imgs]
            images = ";".join(imgs_list)
        elif img0:
            images = img0.get().strip().replace('_200.jpg', '_800.jpg')

        videos = None
        vids = response.css('div.video-wrapper-16-9 > iframe')
        if vids:
            vids_list = [vid.css('::attr(src)').get().strip() for vid in vids]
            videos = ";".join(vids_list)

        price = None
        price_sel = response.css('span.product__price')
        if price_sel:
            price = round(float(price_sel.css('::text').get().strip()[1:])*self.AUD_RATE, 2)

        width, length = self.get_dimensions(title)

        self.prod_ids.add(prod_id)

        result = {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "url": url,
            "source": "My Chemist",
            "product_id": prod_id,
            "existence": existence,
            "title": title,
            "title_en": title,
            "description": description,
            "summary": None,
            "sku": sku,
            "upc": None,
            "brand": None,
            "specifications": None,
            "categories": categories,
            "images": images,
            "videos": videos,
            "price": price,
            "available_qty": 0 if not existence else None,
            "options": None,
            "variants": None,
            "returnable": False,
            "reviews": None,
            "rating": None,
            "sold_count": None,
            "shipping_fee": None,
            "shipping_days_min": 5 if existence else None, # https://www.mychemist.com.au/AboutUs/Shipping
            "shipping_days_max": 5 if existence else None,
            "weight": weight,
            "width": width,
            "height": None,
            "length": length
        }
        # print(result)
        yield result

    def parse_cat_products(self, response: HtmlResponse):
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
        # print(links)
        for l in links:
            yield scrapy.Request(l, headers=self.headers, callback=self.parse)
        
        # print(total_pages, actual_page)
        if actual_page < total_pages:
            next_link = 'https://www.mychemist.com.au'+response.css('a.next-page::attr(href)').get()
            yield scrapy.Request(next_link, headers=self.headers, meta={
                'total_pages': total_pages,
                'actual_pages': actual_page+1
            }, callback=self.parse_cat_products)

    # https://www.mychemist.com.au/categories
    def parse_categories(self, response: HtmlResponse):
        trx = response.css('div#p_lt_ctl07_pageplaceholder_p_lt_ctl00_wCM_AMS_tg_pnltreeTree tbody > tr') # 这里为什么测试时是空的？在网页上找却有很多内容
        cat_links = ['https://www.mychemist.com.au'+tr.css('td span > a::attr(href)').get()+'?size=120'
                     for tr in trx if not tr.css('td img[alt="Expand"], td img[alt="Collapse"]')]
        
        for cl in cat_links:
            yield scrapy.Request(cl, headers=self.headers, callback=self.parse_cat_products)
