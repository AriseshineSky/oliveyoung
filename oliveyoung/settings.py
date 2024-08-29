# Scrapy settings for oliveyoung project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "oliveyoung"

SPIDER_MODULES = ["oliveyoung.spiders"]
NEWSPIDER_MODULE = "oliveyoung.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "oliveyoung (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "oliveyoung.middlewares.OliveyoungSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "oliveyoung.middlewares.OliveyoungDownloaderMiddleware": 543,
#}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "oliveyoung.pipelines.OliveyoungPipeline": 300,
}

MONGO_START_URLS_ITEM = {
    'start_urls': True,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

from urllib.parse import quote_plus
username = quote_plus('admin@everymarket.com')
password = quote_plus('evmkt123!!')
host = '34.172.204.102'
port = '27017'

MONGO_URI = f'mongodb://{username}:{password}@{host}:{port}'
MONGO_DATABASE = 'oliveyoung'
MONGO_COLLECTION = 'categories'
MONGO_AUTHDB = 'admin'

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    # "headless": True,
    "headless": False,
    'args': [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-features=site-per-process', 
    ],
    "slow_mo": 100,  # Slow down Playwright operations by 50 milliseconds
    "timeout": 30 * 1000,  # 30 seconds
}
LOG_FILE = "log/scrapy.log"
# LOG_LEVEL = "ERROR"

CONCURRENT_REQUESTS = 1  # 设置更低的并发请求数
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 3 # 每个上下文中允许的最大页面数量

from playwright.async_api import Request
from scrapy.http.headers import Headers

def custom_headers(
    browser_type: str,
    playwright_request: Request,
    scrapy_headers: Headers,
) -> dict:
    return {
        "Referer": "https://global.oliveyoung.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Cookie": "acesCntry=00; dlvCntry=10; currency=USD; curLang=en; lang=en; FOSID=NTEyZDgzNzYtMWU3Mi00ZWNlLTkwZTUtMGE2MzNjNTM3MzMy; _gcl_au=1.1.2124102817.1716492322; RECENT_VIEW_PRODUCT=%5B%7B%22prdtNo%22%3A%22GA240322465%22%2C%22imagePath%22%3A%22https%3A%2F%2Fimage.globaloliveyoungshop.com%2FprdtImg%2F1065%2F1d976ace-2b3f-4777-b7c7-6f45eb8af0cc.jpg%22%2C%22imageName%22%3A%22Torriden%20Dive-In%20Serum%2050mL%20Refill%20Set%20(%2B50mL%20Refill%20Pack)%22%7D%5D; _ga_5ZDXC4W9LE=GS1.1.1716492358.1.1.1716492358.60.0.0; _scid=5a901744-d42c-4ad5-890f-f2cdd880283c; _scid_r=5a901744-d42c-4ad5-890f-f2cdd880283c; _tt_enable_cookie=1; _ttp=ptr9vTwwrc1THFDynfjsbzBo4Wj; _ga=GA1.2.1710235857.1716492359; _gid=GA1.2.900312979.1716492360; _gat_UA-141211198-1=1; _fbp=fb.1.1716492360016.934803460; _sctr=1%7C1716440400000; _dd_s=rum=0&expire=1716493275225",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" ,
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Priority": "u=0, i"
        }

PLAYWRIGHT_PROCESS_REQUEST_HEADERS = custom_headers


