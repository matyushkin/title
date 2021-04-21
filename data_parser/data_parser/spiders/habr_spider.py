import scrapy


class HabrSpider(scrapy.Spider):
    name = "habr"
    start_urls = ['https://habr.com/ru/hubs/']

    def parse(self, response):
        for hub_url in response.css('.list-snippet__title-link'):
            yield {'hub_url': hub_url.css('a::attr(href)').get()}

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
