import scrapy
from Bs.items import BookScraperItem


class BsSpider(scrapy.Spider):
    name = "BS"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for product in response.css('article.product_pod'):
            product_page_url = response.urljoin(product.css('div.image_container a::attr(href)').get())
            yield scrapy.Request(product_page_url, callback=self.parse_product_page)

        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

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
