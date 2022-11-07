from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from ozon.spiders.items import OzonItemsSpider
from ozon.spiders.links import OzonLinksSpider


def get_data(output='results_raw.json'):
    settings = get_project_settings()
    settings.update({
        "FEEDS": {
            output: {"format": "json", "overwrite": True},
        },
    })

    configure_logging()
    urls = []
    runner = CrawlerRunner(settings)
    d = runner.crawl(OzonLinksSpider, medium=urls)
    d.addCallback(lambda _: runner.crawl(OzonItemsSpider, start_urls=urls))
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def proccess_data(input_file='results_raw.json', output='results_clean.txt'):
    import json
    import pandas as pd

    with open(input_file, 'r') as f:
        result = json.load(f)

    result = [x['os'] for x in result]
    df = pd.DataFrame(result)
    with open(output, 'w') as f:
        f.write(df.value_counts().to_string())


if __name__ == '__main__':
    get_data()
    proccess_data()
