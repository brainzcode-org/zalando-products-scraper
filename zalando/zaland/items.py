# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZalandItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    colour = scrapy.Field()
    images = scrapy.Field()
    manufacturer = scrapy.Field()
    sku = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    variant_sku = scrapy.Field()
    availability = scrapy.Field()
    priceUSD = scrapy.Field()
