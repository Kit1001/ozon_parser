import scrapy


class OzonItemsSpider(scrapy.Spider):
    name = "ozon_items"

    def parse(self, response, **kwargs):
        containers = response.css('dl.x3l')  # div с названием характеристики и ее текстом
        result = ''
        for container in containers:
            items = container.re(r'>(\b[^<>]+)<')  # регулярка забирает весь текст из тегов

            #  если ОС андроид или ios, то как правило есть поле "версия ос",
            #  из которого можно забрать название с версией
            if items[0].lower() == 'версия android' or items[0].lower() == 'версия ios':
                result = items[1]
                break

            #  если ОС не андроид или ios, то берем название из поля "операционная система"
            elif items[0].lower() == 'операционная система' and not result:
                result = items[1]

        if not result:
            result = f'Не удалось узнать тип ОС, либо не указана'

        yield {
            'os': result,
            'url': response.url
        }
