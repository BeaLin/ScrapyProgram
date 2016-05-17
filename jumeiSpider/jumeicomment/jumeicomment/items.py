# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JumeicommentItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    product_id=Field()
    product_name=Field()
    user_name = Field()
    user_detail = Field()
    user_comment = Field()
    comment_time = Field()
    
