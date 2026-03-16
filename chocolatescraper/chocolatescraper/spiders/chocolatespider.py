import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all-products"]

    def parse(self, response):
        products = response.css('product-item')

        # format for data scraped into a dictionary
        for product in products:
            yield {
                'name': product.css('a.product-item-meta__title::text').get(),
                "price": product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', '').replace('\n</span>', '').replace('</span>', '').replace('<span class=\"price price--highlight\">\n              <span class=\"visually-hidden\">', '').replace('From', '').replace('Sale price', ''),
                'url': product.css('div.product-item-meta a').attrib['href'],
            }

        # for scraping from all pages using pagination

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page 
            yield response.follow(next_page_url, callback=self.parse)