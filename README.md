# ozon_parser
Парсер собирает информацию об ОС на 100 самых популярных смартфонах

Стек: Python, Scrapy, Selenium, pandas

Запуск через main.py, необработанные данные сохраняются в results_raw.json, построенное распределение моделей устройств по версиям операционных систем - в файле results_clean.txt

Не использовал прокси, т.к. нет доступа к хорошим, а бесплатные сразу триггерят cloudflare, но весь функционал настроен, нужно только раскоментить настройки и добавить список рабочих адресов.
