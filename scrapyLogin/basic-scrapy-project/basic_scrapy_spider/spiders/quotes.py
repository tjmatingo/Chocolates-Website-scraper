from collections.abc import Iterable
from typing import Any

import scrapy
from basic_scrapy_spider.items import QuoteItem
from http import cookies
from scrapy import Spider
from scrapy.http import FormRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        login_url = "https://quotes.toscrape.com/login"
        yield scrapy.Request(login_url, callback=self.login)

    def login(self, response):
        token = response.css("form input[name=csrf_token]::attr(value)").extract_first()
        yield FormRequest.from_response(response, 
                                        formdata={'csrf_token': token,
                                                  'password': 'foobar',
                                                  'username': 'foobar'},
                                        callback=self.start_scraping)

    def start_scraping(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }