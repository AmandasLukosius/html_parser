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
    # Doktorantai
    vardas_pavarde = scrapy.Field()
    d_tema = scrapy.Field()
    stud_metai = scrapy.Field()

    # Vadovai
    vadovas = scrapy.Field()
    # v_padalinys = scrapy.Field()
    # v_pareigos = scrapy.Field()
    # v_adresas = scrapy.Field()
    # v_telefonas = scrapy.Field()
    # v_e_pastas = scrapy.Field()
    # v_puslapis = scrapy.Field()
    pass