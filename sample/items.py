# -*- coding: utf-8 -*-

import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()

