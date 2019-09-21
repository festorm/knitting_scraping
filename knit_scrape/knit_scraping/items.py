# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst, Compose

class KnitScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    filter_empty = lambda x: x if x else None
    
    page = Field(input_processor=MapCompose(str,.strip, filter_empty))
    title = Field(input_processor=MapCompose(str.strip, filter_empty))
    price = Field(input_processor=MapCompose(str.strip, filter_empty))
    language = Field(input_processor=MapCompose(str.strip, filter_empty))
    description = Field(input_processor=MapCompose(str.strip, filter_empty))
    size_guides = Field(input_processor=MapCompose(str.strip, filter_empty))
    size_available = Field(input_processor=MapCompose(str.strip, filter_empty))
    size = Field(input_processor=MapCompose(str.strip, filter_empty))
    knitting_gauge = Field(input_processor=MapCompose(str.strip, filter_empty))
    yarn = Field(input_processor=MapCompose(str.strip, filter_empty))

    url = Field(input_processor=TakeFirst())
    body = Field(input_processor=MapCompose(str.strip, filter_empty))
    scrape_date = Field()

