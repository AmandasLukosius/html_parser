import scrapy
from scrapy.selector import Selector
from Html_parser.items import HtmlParserItem
from urllib.parse import urljoin

class uniSpider(scrapy.Spider):
	name = "dok_sarasai"
	allowed_domains = ["mii.lt"]
	
	def start_requests(self):
		urls = [
		'https://www.mii.lt/doktorantura/doktorantu-sarasai'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback= self.parse, dont_filter = True)
	
	def parse(self, response):
		puslapiai = response.xpath('//div[contains(@class, "accordion-heading panel-heading")]/a/@href').extract()
		for p in puslapiai:
			yield scrapy.Request(p, callback=self.parse_puslapius)

	def parse_puslapius(self, response):
		doktorantai = response.xpath('//div[contains(@class, "accordion-inner panel-body")]/table//tr')
		for doktorantas in doktorantai[1:]:
			item = HtmlParserItem()
			item['vardas_pavarde'] = doktorantas.xpath('td[1]//text()').extract()
			item['vadovas'] = doktorantas.xpath('td[2]//text()').extract()
			item['stud_metai'] = " ".join(doktorantas.xpath('td[3]//text()').extract())
			yield item