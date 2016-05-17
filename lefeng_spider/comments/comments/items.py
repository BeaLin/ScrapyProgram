# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CommentsItem(Item):
    createdAt = Field()
    id = Field()
    productId = Field()
    productId2 = Field()
    productScore = Field()

    remark = Field()
    reply = Field()
    type = Field()
    userId = Field()
    userName=Field()
