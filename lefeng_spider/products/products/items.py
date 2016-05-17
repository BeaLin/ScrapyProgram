# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductsItem(Item):
    #about brand
    brandId = Field()
    brandName = Field()
    brandUrl = Field()

    #about product
    productId = Field()
    productName = Field()
    marketPrice = Field()
    salePrice = Field()
    imgUrl = Field()
    commentNumber = Field()
