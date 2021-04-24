import pickle
import pandas
import scrapy

path = '/home/leo/Yandex.Disk/GitHub/DATASETS/META/it_articles_ru.feather'
df = pandas.read_feather(path)
df_habr = [df['source'] == 'habr']


class HabrSpider(scrapy.Spider):
    name = "habr_full"
    start_urls = df_habr['index'].to_list()[:5]

    def parse(self, response):
        for card in response.css('article.post_preview'):
            yield {
                'filename': response.request.url,
                'fulltext': card.css('.post__body_full::text').get()
            }
