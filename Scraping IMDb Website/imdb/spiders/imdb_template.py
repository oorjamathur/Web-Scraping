import scrapy
from scrapy.http import request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ImdbTemplateSpider(CrawlSpider):
    name = 'imdb_template'
    allowed_domains = ['imdb.com']
    #start_urls = []
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[1]")), process_request='set_user_agent') #no callbacks specified ere since 1st one is already doing it
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request


    def parse_item(self, response):
        yield{
            'name': response.xpath("//div[@class='TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt']/h1/text()").get(),
            'year': response.xpath("//span[@class='TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex']/text()").get(),
            'duration': response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt']/li[3]/text()").get(),
            'genre': response.xpath("//a[@class='GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt']/span/text()").getall(),
            'movie_url': response.url,
            'User-Agent': response.request.headers['User-Agent']
        }
