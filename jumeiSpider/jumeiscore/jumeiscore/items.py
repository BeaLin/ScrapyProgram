# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JumeiscoreItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_id=Field()
    product_name=Field()
    koubei_count=Field()
    comment_count=Field()
    avarage_rating = Field()
    detail_score=Field()
    skin_part=Field()
