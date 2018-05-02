# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from collections import OrderedDict

import scrapy


class HtmlParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vardas_pavarde = scrapy.Field()
    d_tema = scrapy.Field()
    vadovas = scrapy.Field()
    stud_metai = scrapy.Field()
    pass