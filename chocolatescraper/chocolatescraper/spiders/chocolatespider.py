from collections.abc import Iterable
from typing import Any

import scrapy
from chocolatescraper.items import ChocolateProductScraper
from chocolatescraper.itemloaders import ChocolateProductloader
from urllib.parse import urlencode

API_KEY = '28c0b581-5cbd-415b-b747-d506a9bc09e2'

def get_proxy_url(url):
    payload = {'api_key' : API_KEY, 'url': url}
    base_url = 'https://proxy.scrapeops.io/v1/'
    proxy_url = base_url + '?' + urlencode(payload)
    return proxy_url


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk","proxy.scrapeops.io",]
    # start_urls = ["https://www.chocolate.co.uk/collections/all-products"]

    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all-products'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)


    async def start(self):
        async for r in super().start():
            yield r

    def parse(self, response):
        products = response.css('product-item')

        # # organizing items
        # product_item = ChocolateProductScraper()

        # format for data scraped into a dictionary
        for product in products:

            chocolate = ChocolateProductloader(item=ChocolateProductScraper(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text')
            chocolate.add_css('price',  'span.price::text', re=r'£?(\d+(?:\.\d+)?)')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            
            yield chocolate.load_item()

        # for scraping from all pages using pagination

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page 
            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)