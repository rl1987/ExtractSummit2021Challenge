import scrapy

from urllib.parse import urljoin, urlparse
import json

from challenge.items import ChallengeItem

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

        next_page_link = response.xpath('//a[.//h2[contains(text(), "Next Page")]]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_product_list)

    def parse_product_page(self, response):
        item = ChallengeItem()
        
        item['item_id'] = response.xpath("//span[@id='uuid']/text()").get()
        item['name'] = response.xpath('//div[@class="left-content"]/h2/text()').get()
        item['flavor'] = response.xpath("//p[contains(text(), 'Flavor:')]/span/text()").get() # TODO: some products need API call for this
        
        image_path = response.xpath('//div[@class="right-image"]/img/@src').get()

        if image_path is not None:
            image_filename = image_path.split('/')[-1]
            image_id = image_filename.split('.')[0]
            item['image_id'] = image_id


        if item.get('flavor') is not None and item.get('flavor') != 'NO FLAVOR':
            yield item
        else:
            api_url = response.xpath('//span[@class="flavor"]/@data-flavor').get()
            api_url = urljoin(response.url, api_url)
            
            meta_dict = {'item' : item}

            yield scrapy.Request(api_url, meta=meta_dict, callback=self.parse_product_flavor)

    def parse_product_flavor(self, response):
        meta_dict = response.meta
        item = meta_dict.get('item')

        json_str = response.text
        json_dict = json.loads(json_str)

        flavor = json_dict.get('value')

        item['flavor'] = flavor

        yield item

