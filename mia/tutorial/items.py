# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
import scrapy


class miaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_name= Field()
    goods_standard= Field()
    goods_detail=Field()
    producting_area= Field()
    composition= Field()
    use= Field()
    mia_viewpoint= Field()
    article_number= Field()
    weight= Field()
    tax_rate= Field()
    goods_label= Field()
    level_workshop_price= Field()
    price= Field()
    good_reputation_rating= Field()
    month_sale_number= Field()
    store_number= Field()
    tariffs_detail= Field()
    goods_url= Field()
    goods_picture= Field()
    advantage_picture= Field()
    voedingsinformatie_picture= Field()
    instructions_picture= Field()
    authentication_picture= Field()
    media_publicity_picture= Field()
    warehouse_logistics_picture= Field()
    wrap_picture= Field()
    use_age= Field()
    root_type= Field()
    super_type= Field()
    child_type= Field()
    image_url= Field()
    images_urls= Field()
    comments_time= Field()
    comments_content= Field()
    comments_imgs= Field()
    user_type=Field()
    crawling_time=Field()
    goods_brand_name= Field()
    sites_url= Field()
    sites_logo= Field()
    sites_chinese_name= Field()


