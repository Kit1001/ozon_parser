# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from importlib import import_module
from time import sleep

from scrapy import signals
# useful for handling different item types with a single interface
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType


class OzonSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class OzonDownloaderMiddleware:

    def __init__(self, driver_name, driver_arguments):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_arguments: list
            A list of arguments to initialize the driver
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        self.driver_cls = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        self.options = driver_options

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not driver_name:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            driver_name=driver_name,
            driver_arguments=driver_arguments,
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        proxy = request.meta.get('proxy')
        if proxy:
            self.options.proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy,
                'sslProxy': proxy,
                'noProxy': ''})

        with self.driver_cls(options=self.options) as driver:
            time.sleep(random.randint(0, 3))
            driver.get(request.url)

            for cookie_name, cookie_value in request.cookies.items():
                driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            # Ожидаем полной загрузки страницы
            # Не использовал WebDriverWait, т.к. он прерывается раньше, чем JS действительно загрузит весь контент
            len_ex = -1
            while len(driver.page_source) != len_ex:
                len_ex = len(driver.page_source)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(random.randint(3, 6))

            body = str.encode(driver.page_source)

            return HtmlResponse(
                driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        pass
