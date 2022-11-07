# Scrapy settings for ozon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'ozon'
SPIDER_MODULES = ['ozon.spiders']
NEWSPIDER_MODULE = 'ozon.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 4
# прокси отключены, т.к. нет возможности проверить с нормальным прокси, а бесплатные сразу триггерят cloudflare
DOWNLOADER_MIDDLEWARES = {
   # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
   # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
   'ozon.middlewares.OzonDownloaderMiddleware': 543,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_ARGUMENTS = ['-headless']  # '--headless' if using chrome instead of firefox
LOG_LEVEL = 'INFO'
ITEM_LIMIT = 100  # количество телефонов, информацию о которых нужно собрать

# ROTATING_PROXY_LIST = [
#     'proxy1.com:8000',
#     'proxy2.com:8031',
#     # ...
# ]
