# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TouristspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'tourist'
    title = scrapy.Field()
    avatar = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    create_info = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()

