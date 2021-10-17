import scrapy
from scrapy.http import request


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        
        countries = response.xpath('//td/a')
        for c in countries:
            name = c.xpath('.//text()').get()
            link = c.xpath('.//@href').get()
            # yield {
            #     'country_name': name,
            #     'country_link': link
            # }

        #converting relative links to absolute
        #abs_link = f'https://www.worldometers.info{link}'
            #OR
            #abs_link = response.urljoin(link)

            # to go to the links (redirected ones) actually
            #yield scrapy.Request(url=abs_link)

            # Don't want to convert to abs link
            yield response.follow(link, callback = self.parse_country, meta = {'name':name}) # passing args available inside parse method to parse_country using meta
        
            # same thing achieved with all the 3 methods

    def parse_country(self, response):
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        name = response.request.meta['name']
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            pop = row.xpath('.//td[2]/strong/text()').get()
            
            yield{
                'name': name,
                'year':year,
                'population':pop
            }