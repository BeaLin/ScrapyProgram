# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OmtaoItem(scrapy.Item):

    goods_id= scrapy.Field()
    goods_name= scrapy.Field()
    sites_url= scrapy.Field()
    goods_picture= scrapy.Field()
    level_workshop_price= scrapy.Field()
    price= scrapy.Field()
    month_sale_number= scrapy.Field()
    root_type= scrapy.Field()
    goods_brand_name= scrapy.Field()
    producting_area= scrapy.Field()
    goods_standard= scrapy.Field()


    goods_label= scrapy.Field()

    good_reputation_rating= scrapy.Field()

    tariffs_detail= scrapy.Field()



    for_peaple=scrapy.Field()
    goods_code=scrapy.Field()

    #advantage_picture= scrapy.Field()
    #voedingsinformatie_picture= scrapy.Field()
    #instructions_picture= scrapy.Field()
    #authentication_picture= scrapy.Field()
    #media_publicity_picture= scrapy.Field()
    #warehouse_logistics_picture= scrapy.Field()
    #wrap_picture= scrapy.Field()
    #article_number= scrapy.Field()
    #weight= scrapy.Field()
    #tax_rate= scrapy.Field()
    #root_type_id= scrapy.Field()
    #parent_type_id= scrapy.Field()
    #child_type_id= scrapy.Field()
    #super_type= scrapy.Field()
    #child_type= scrapy.Field()
    #comments_time= scrapy.Field()
    #crawling_time= scrapy.Field()
    #comments_content= scrapy.Field()
    #goods_brand_id= scrapy.Field()
    #brand_id= scrapy.Field()
    #type_id= scrapy.Field()
    #composition= scrapy.Field()
    #sites_logo= scrapy.Field()
    #sites_chinese_name= scrapy.Field()
    #store_number= scrapy.Field()
