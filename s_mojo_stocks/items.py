# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SMojoStocksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StockDetails(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    companyName = scrapy.Field()
    price = scrapy.Field()
    valuation = scrapy.Field()
    quality = scrapy.Field()
    technicals = scrapy.Field()
    fintrend = scrapy.Field()
    value = scrapy.Field()
    call_type = scrapy.Field()
