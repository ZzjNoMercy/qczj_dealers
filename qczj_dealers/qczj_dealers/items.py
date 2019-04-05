# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QczjDealersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dealer_name = scrapy.Field()
    dealer_city = scrapy.Field()
    dealer_class = scrapy.Field()
    dealer_phone = scrapy.Field()
    dealer_addr = scrapy.Field()
    dealer_brands = scrapy.Field()

class QczjPriceItem(scrapy.Item):
    dealer_name = scrapy.Field()
    model_name = scrapy.Field()
    type_name = scrapy.Field()
    guide_price = scrapy.Field()
    promotion_price = scrapy.Field()
