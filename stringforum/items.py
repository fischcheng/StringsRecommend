# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StringRating(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rts = scrapy.Field()
    Durability = scrapy.Field()
    Power = scrapy.Field()
    Control = scrapy.Field()
    Feel = scrapy.Field()
    Comfort = scrapy.Field()
    Spin= scrapy.Field()
    Tension_Stability=scrapy.Field()
    Overall=scrapy.Field()
    PPR=scrapy.Field()
