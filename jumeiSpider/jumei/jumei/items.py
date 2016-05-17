# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class JumeiItem(scrapy.Item):

    category = Field()
    categoryId = Field()

    categoryUrl = Field()

    productId = Field()
    brandId = Field()
    productType = Field()

    productName = Field()
    productUrl = Field()

    originalPrice = Field()
    realPrice = Field()

    purchaserNumber = Field()
    imageUrl = Field()
    timeCountdown = Field()

    brand = Field()
    function = Field()
    forPeople = Field()
    specification = Field()
    location = Field()

    avarage_rating = Field()
    qingshuang_rating = Field()
    ziran_rating = Field()
    chijiu_rating = Field()
    zexia_rating = Field()
    skin_mix=Field()
    skin_soul = Field()
    skin_dry = Field()
    skin_middle = Field()
    skin_sensitive = Field()


