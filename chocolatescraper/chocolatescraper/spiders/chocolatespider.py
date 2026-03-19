import scrapy
from chocolatescraper.items import ChocolateProductScraper
from chocolatescraper.itemloaders import ChocolateProductloader

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all-products"]

    def parse(self, response):
        products = response.css('product-item')

        # # organizing items
        # product_item = ChocolateProductScraper()

        # format for data scraped into a dictionary
        for product in products:

            chocolate = ChocolateProductloader(item=ChocolateProductScraper(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)'),
            
            yield chocolate.load_item()

        # for scraping from all pages using pagination

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page 
            yield response.follow(next_page_url, callback=self.parse)