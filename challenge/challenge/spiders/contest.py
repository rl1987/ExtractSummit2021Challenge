import scrapy


class ContestSpider(scrapy.Spider):
    name = 'contest'
    allowed_domains = ['contest-646508-5umjfyjn4a-ue.a.run.app']
    start_urls = ['http://contest-646508-5umjfyjn4a-ue.a.run.app/']

    def parse(self, response):
        pass
