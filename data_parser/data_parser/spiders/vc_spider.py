import scrapy

class VCSpider(scrapy.Spider):
    name = "vc"
    start_urls = [f'https://vc.ru/{i}' for i in range(36701, 237853)] 

    def parse(self, response):
        yield {
            'url': response.request.url,
            'title': response.css('h1::text').get().strip(),
            'post_time': response.css('time::attr(title)').get().strip(),
            'summary': response.css('.content--full').xpath('string(.//div//p)').get().strip(),
            'views_num': response.css('.views__value::text').get().strip(),
            'comments_num': response.css('.comments_counter__count__value::text').get().strip()
        }