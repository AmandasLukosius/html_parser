import scrapy
from scrapy.selector import Selector
from Html_parser.items import HtmlParserItem

class uniSpider(scrapy.Spider):
	name = "doktorantas"
	allowed_domains = ["mii.lt"]
	
	def start_requests(self):
		urls = [
		'https://www.mii.lt/struktura/darbuotojai/287-beresnevicius-gytautas'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback= self.parse)
	
	def parse(self, response):
		# for titles in response.xpath('//div[contains(@class, "category-headline-item")]'):
		item = HtmlParserItem()
		item['d_tema'] = response.xpath('//*[@id="disertacija"]/div/p[1]/text()').extract()
		item['vadovas'] = response.xpath('//*[@id="disertacija"]/div/p[2]/a/text()').extract()[0]
		item['stud_metai'] = response.xpath('//*[@id="disertacija"]/div/p[3]/text()').extract()[0]
		# yield item