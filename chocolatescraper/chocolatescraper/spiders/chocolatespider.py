import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolates.co.uk"]
    start_urls = ["https://chocolates.co.uk"]

    def parse(self, response):
        pass
