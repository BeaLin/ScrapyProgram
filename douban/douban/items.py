# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    book_name= scrapy.Field()
    book_url= scrapy.Field()
    book_author= scrapy.Field()
    review_author= scrapy.Field()
    review_score= scrapy.Field()
    review= scrapy.Field()




