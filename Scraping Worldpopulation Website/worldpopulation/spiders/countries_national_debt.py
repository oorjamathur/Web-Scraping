import scrapy


class CountriesNationalDebtSpider(scrapy.Spider):
    name = 'countries_national_debt'
    allowed_domains = ['worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//table/tbody/tr")
        for c in countries:
            name = c.xpath('.//td[1]/a/text()').get()
            gdp = c.xpath('.//td[2]/text()').get()
            yield{
                'name':name,
                'gdp':gdp
            }
