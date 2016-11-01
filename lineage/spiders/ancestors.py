# -*- coding: utf-8 -*-
import scrapy


class AncestorsSpider(scrapy.Spider):
    name = "ancestors"
    allowed_domains = ["www.genealogy.math.ndsu.nodak.edu"]

    def start_requests(self):
        url = 'https://www.genealogy.math.ndsu.nodak.edu/id.php?id='
        start_id = getattr(self, 'start-id', None)
        if start_id is not None:
            url += start_id
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for advisor in response.xpath("//p[text()[contains(.,'Advisor')]]/a"):
            name = advisor.css("a::text").extract_first(),
            url = 'https://www.genealogy.math.ndsu.nodak.edu/'
            url += advisor.css("a::attr(href)").extract_first()
            yield {'name':name, 'url':url, 'child':response.request.url}
            yield scrapy.Request(url, callback=self.parse)
