from datetime import datetime
from re import findall
import scrapy
from scrapy.http import HtmlResponse

class MyChemistSpider(scrapy.Spider):
    name = "mychemist"
    allowed_domains = ['mychemist.com.au']
    start_urls = []

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

    def get_product_id(self, url: str):
        id_match = findall(r'buy/(\d+)', url)
        if id_match:
            return id_match[0]
    
    def get_title(self, text: str):
        title_match = findall(r'Buy\s+(.*)\s+Online at Chemist Warehouse', text)
        if title_match:
            return title_match[0]
        
    def parse(self, response: HtmlResponse):
        url = response.css('link[rel="canonical"]::attr(href)').get().strip()

        existence = True
        if 'no longer available' in response.css('div[style="margin:auto ; color:red ; font-size:20px ; text-align:left ; font-weight:bold"]::text').get().lower():
            existence = False
        
        title = self.get_title(response.css('title').get())

        # TODO
        description = None

        cats_list = [cat.css("::text").get().strip() for cat in response.css('div.breadcrumbs > a')[1:]]
        categories = " > ".join(cats_list)

        images = None
        if existence:
            imgs = response.css('div.sub_images img')
            img0 = response.css('div#this_slider img::attr(src)')
            if imgs:
                imgs_list = [img.css('::attr(src)').get().strip().replace('_50.jpg', '_800.jpg') for img in imgs]
                images = ";".join(imgs_list)
            elif img0:
                images = img0.get().strip().replace('_200.jpg', '_800.jpg')

        videos = None
        if existence:
            vids = response.css('div.video-wrapper-16-9 > iframe')
            if vids:
                vids_list = [vid.css('::attr(src)').get().strip() for vid in vids]
                videos = ";".join(vids_list)

        price = None
        if existence:
            price = round(float(response.css('span.product__price').get().strip()[1:])*self.AUD_RATE, 2)

        yield {
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "url": url,
            "source": "My Chemist",
            "product_id": self.get_product_id(url),
            "existence": existence,
            "title": title,
            "title_en": title,
            "description": description,
            "summary": None,
            "sku": response.css('div.product-id').get().split(':')[1].strip(),
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
            
        }
