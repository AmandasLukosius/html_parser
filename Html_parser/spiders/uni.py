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
		domain = 'https://www.mii.lt'
		name = response.meta['name']
		item = HtmlParserItem()
		item['vardas_pavarde'] = name.strip()

		sarasas = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Preliminari")]/descendant::text()').extract()
		item['d_tema'] = sarasas[-1]
		# if not item['d_tema']:
		# 	item['d_tema'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Preliminari")]/descendant::text()').extract()[1]
		# 	if not item['d_tema']:
		# 		item['d_tema'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Preliminari")]/descendant::text()').extract()[2]

		try:
			item['vadovas'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Vadovas")]/descendant::text()').extract()[1]
		except:
			item['vadovas'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Vadovas")]/a/text()').extract()

		if '\xa0' in item['vadovas']:
			item['vadovas'] = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Vadovas")]/descendant::text()').extract()[2]

		metai = response.xpath('//div[@id="doktoranturos-studijos"]/div/p[contains(strong, "Studij")]/descendant::text()').extract()
		metai =  list(filter(None, metai))
		item['stud_metai'] = metai

		url = response.xpath('//*[@id="disertacija"]/div/p[contains(strong, "Vadovas")]/a/@href').extract()
		new_url = urljoin(domain, url)
		# yield scrapy.Request(new_url, callback=self.parse_vadova)
		return item

	# def parse_vadova(self, response):
	# 	item = HtmlParserItem()
	# 	item['v_padalinys'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[contains(text(), "Padalinys")]/a/text()').extract()
	# 	item['v_pareigos'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[3]/text()[2]').extract()
	# 	item['v_adresas'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[contains(text(), "Dirba")]/text()').extract_first()
	# 	item['v_telefonas'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[contains(text(), "Telefonas")]/text()').extract()
	# 	item['v_e_pastas'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[contains(text(), "Elektroninis")]/a[1]/text()').extract()
	# 	item['v_puslapis'] = response.xpath('//*[@id="page-component"]/div/div[3]/p[contains(text(), "puslapis")]/text()[5]').extract()
	# 	return item