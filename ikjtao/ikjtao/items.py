# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IkjtaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #about category
    supCategory = scrapy.Field()
    supCategoryUrl = scrapy.Field()
    # subCategory = scrapy.Field()
    # subCategoryUrl= scrapy.Field()
    # threeCategory = scrapy.Field()
    # threeCategoryUrl = scrapy.Field()

    #about product in product list of a certain category
    productName = scrapy.Field()
    productId = scrapy.Field()
    productUrl = scrapy.Field()
    productImageUrl = scrapy.Field()
    productSalePrice = scrapy.Field()
    productMarketPrice =scrapy.Field()
    salesVolume = scrapy.Field()
    commentNum = scrapy.Field()
    #currentUrl = scrapy.Field()

    #single page of a certain product
    monthlySales = scrapy.Field()
    brand = scrapy.Field()
    location = scrapy.Field()
    composition = scrapy.Field()
    application = scrapy.Field()
    itemNo = scrapy.Field()
    commodityBrand = scrapy.Field()
    weight = scrapy.Field()
    taxRate = scrapy.Field()
    tag = scrapy.Field()


    pass
