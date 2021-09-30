import scrapy

from urllib.parse import urljoin, urlparse

class ContestSpider(scrapy.Spider):
    name = 'contest'
    allowed_domains = ['contest-646508-5umjfyjn4a-ue.a.run.app']
    start_urls = ['https://contest-646508-5umjfyjn4a-ue.a.run.app/listing?page=-1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_product_list)

    def parse_product_list(self, response):
        for product_link in response.xpath('//a[contains(@href, "/listing/i/")]/@href').getall():
            product_url = urljoin(response.url, product_link)
            yield scrapy.Request(product_url, callback=self.parse_product_page)

        next_page_link = response.xpath('//a[contains(@href, "page=")]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_product_list)

    def parse_product_page(self, response):
        pass
