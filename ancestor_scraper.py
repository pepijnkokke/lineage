# -*- coding: utf-8 -*-
import scrapy

class AncestorsSpider(scrapy.Spider):
    name = "ancestors"
    allowed_domains = ["www.genealogy.math.ndsu.nodak.edu"]

    def start_requests(self):
        href = 'https://www.genealogy.math.ndsu.nodak.edu/id.php?id='
        start_id = getattr(self, 'start-id', None)
        if start_id is not None:
            href += start_id
            yield scrapy.Request(href, self.parse)

    def parse(self, response):

        # Extract the NAME of the Ph.D. candidate
        misc = " - The Mathematics Genealogy Project"
        name = response.xpath("//title/text()")
        name = name.extract_first()
        name = name[:-len(misc)]

        # Extract the YEAR of graduation
        year = response.xpath('//div[img/@src[contains(.,img/flags)]]/span/text()')
        year = year.re("\\d\\d\\d\\d")
        if year:
            year = min([int(y) for y in year])
        else:
            year = None

        # Extract the HREF of the entry
        href = response.request.url

        # Extract the ADVISORS
        advisors = dict()
        for advisor in response.xpath("//p[text()[contains(.,'Advisor')]]/a"):
            advisor_name = advisor.css("a::text").extract_first()
            advisor_href = 'https://www.genealogy.math.ndsu.nodak.edu/'
            advisor_href += advisor.css("a::attr(href)").extract_first()
            advisors.update({advisor_name: advisor_href})

        yield {
            u'name'     : name,
            u'year'     : year,
            u'href'     : href,
            u'advisors' : advisors
        }

        for advisor_name, advisor_href in advisors.iteritems():
            yield scrapy.Request(advisor_href, callback=self.parse)
