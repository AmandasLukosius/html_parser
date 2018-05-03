import scrapy
from scrapy.selector import Selector
from Html_parser.items import HtmlParserItem
from urllib.parse import urljoin

class uniSpider(scrapy.Spider):
	name = "doktorantas"
	allowed_domains = ["mii.lt"]
	
	def start_requests(self):
		urls = [
		'https://www.mii.lt/struktura/darbuotojai/pagal-pareigas'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback= self.parse)
	
	def parse(self, response):
		domain = 'https://www.mii.lt'
		doktorantai = response.xpath('//li[@class="cat-list-row1 clearfix" and contains(h3, "Doktorantai")]/ul/li[contains(@class, "cat-list-row0 clearfix")]/h3/a/@href').extract()
		for d in doktorantai:
			url = urljoin(domain, d)
			name = response.xpath('//li[@class="cat-list-row1 clearfix" and contains(h3, "Doktorantai")]/ul/li[contains(@class, "cat-list-row0 clearfix")]/h3/a/text()').extract()[doktorantai.index(d)]
			yield scrapy.Request(url, meta={'name': name}, callback=self.parse_doktorantus)

	def parse_doktorantus(self, response):
		name = response.meta['name']
		item = HtmlParserItem()
		item['vardas_pavarde'] = name.strip()
		item['d_tema'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Preliminari")]/text()').extract()
		item['vadovas'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Vadovas")]/descendant-or-self::text()').extract()[1]
		item['stud_metai'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "laikas")]/text()').extract()
		return item