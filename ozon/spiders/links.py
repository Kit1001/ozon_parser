import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings


class OzonLinksSpider(scrapy.Spider):
    name = "ozon_links"
    page = 1
    item_count = 0
    item_limit = get_project_settings().get('ITEM_LIMIT')
    start_urls = ['https://www.ozon.ru/category/smartfony-15502/?sorting=rating']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #  для передачи ссылок в другой spider используется список, который получаем аргументом при создании паука
        self.medium = kwargs.get('medium')

    def parse(self, response, **kwargs):
        links = response.css('.rk3.r3k a.k8n::attr(href)')
        for link in links:
            self.item_count += 1
            if self.item_count <= self.item_limit:
                clean_link = response.urljoin(link.get().split('?')[0])
                if self.medium is not None:
                    self.medium.append(clean_link)
            else:
                raise CloseSpider('Item limit reached')

        self.page += 1
        url = f'https://www.ozon.ru/category/smartfony-15502/?page={self.page}&sorting=rating'
        yield Request(url=url, callback=self.parse)
