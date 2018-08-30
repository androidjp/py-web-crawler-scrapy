# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppJuejinItem(scrapy.Item):
    # title
    title = scrapy.Field()
    # link
    url = scrapy.Field()
    pass
