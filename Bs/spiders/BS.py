import scrapy
import random
from Bs.items import BookScraperItem

# Define your user agents
USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'),  # chrome
]

class BsSpider(scrapy.Spider):
    name = "BS"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)}, callback=self.parse)

    def parse(self, response):
        for product in response.css('article.product_pod'):
            product_page_url = response.urljoin(product.css('div.image_container a::attr(href)').get())
            yield scrapy.Request(product_page_url, headers={'User-Agent': random.choice(USER_AGENTS)}, callback=self.parse_product_page)

        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), headers={'User-Agent': random.choice(USER_AGENTS)}, callback=self.parse)

    def parse_product_page(self, response):
        item = BookScraperItem()
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('p.price_color::text').get()

        availability_text = response.css('p.instock.availability::text').getall()
        item['availability'] = ' '.join([text.strip() for text in availability_text if text.strip()])

        item['rating'] = response.css('p.star-rating::attr(class)').get().split()[-1]
        item['image_url'] = response.urljoin(response.css('div.item.active img::attr(src)').get())
        item['product_page_url'] = response.url
        item['upc'] = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        item['product_type'] = response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').get()
        item['price_excl_tax'] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').get()
        item['price_incl_tax'] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get()
        item['tax'] = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').get()
        item['number_of_reviews'] = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').get()
        yield item
