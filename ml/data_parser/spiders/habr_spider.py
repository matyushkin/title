import pickle
import pandas
import scrapy


class HabrSpider(scrapy.Spider):
    name = "habr"

    def hubs_urls():
        with open('habr_hubs.pickle', 'rb') as f:
            start = 'https://habr.com/ru/hub/'
            urls = [f'{start}{hub}' for hub in pickle.load(f)]
        return urls

    start_urls = hubs_urls()

    def parse(self, response):
        for card in response.css('article.post_preview'):
            yield {
                'title': card.css('.post__title_link::text').get(),
                'url': card.css('.post__title_link::attr(href)').get(),
                'post_time': card.css('.post__time::text').get(),
                'summary': card.xpath('string(.//div|.//div//p)').get(),
                'likes_num': card.css('.post-stats__result-counter::text').get(),
                'favs_num': card.css('.bookmark__counter::text').get(),
                'views_num': card.css('.post-stats__views-count::text').get(),
                'comments_num': card.css('.post-stats__comments-count::text').get()
            }
        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


