import re
import scrapy

class NewsSpider(scrapy.Spider):
    name = 'feedsnews'
    start_urls = ['http://financenews.com.br/feed/', 'https://www.ultimoinstante.com.br/feed/']
    quotation_mark_pattern = re.compile(r'“|”')

    def parse(self, response):
        for channel in response.xpath('//channel'):
            titles    = channel.xpath('//item/title/text()').getall()
            #links   = channel.xpath('//item/link/text()').getall()
            # NOTE: passar list para o flask
            self.quotes_list.append(titles)

        next_page = response.xpath('//channel/item/link/text()').extract()
        if next_page is not None:
            yield response.follow(next_page)