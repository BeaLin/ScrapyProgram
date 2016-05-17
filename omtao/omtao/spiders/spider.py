# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from omtao.items import OmtaoItem
from scrapy.selector import Selector
from scrapy import Request

class OmtaoSpider(Spider):
    name = "omtao"
    allowed_domains = ["www.omtao.com"]
    start_urls = [
		"http://www.omtao.com/baby.html",
        "http://www.omtao.com/health.html"

    ]
    def check_list(self,list):
        if list:
            return list[0]
        else:
            return ''

    def parse(self,response):
        items=[]
        sites1=response.xpath('//div[@class="p-lview"]/div[@class="p-item"]')
        for site in sites1:
            url=self.check_list(site.xpath('div[@class="p-left"]/a/@href').extract())
            sites_url="http://www.omtao.com"+url
            goods_id=url.split('/')[-1].split(".")[0]
            goods_picture=self.check_list(site.xpath('div[@class="p-left"]/a/img/@data-original').extract())
            goods_name=self.check_list(site.xpath('div[@class="p-right"]/div[@class="p-name"]/a/text()').extract())
            price=self.check_list(site.xpath('div[@class="p-right"]/div[@class="p-price"]/span/text()').extract())
            level_workshop_price=self.check_list(site.xpath('div[@class="p-right"]/div[@class="p-price"]/strong/text()').extract())
            r = Request(sites_url ,meta={'sites_url':sites_url,'goods_id':goods_id,'goods_picture':goods_picture,'goods_name':goods_name,'price':price,'level_workshop_price':level_workshop_price} ,callback=self.parse_info)
            items.append(r)
        sites2=response.xpath('//div[@class="p-gview"]/div')
        for site in sites2:
            url=self.check_list(site.xpath('div[@class="p-img"]/a/@href').extract())
            goods_picture=self.check_list(site.xpath('div[@class="p-img"]/a/img/@data-original').extract())
            sites_url="http://www.omtao.com"+url
            goods_id=url.split('/')[-1].split(".")[0]
            goods_name=self.check_list(site.xpath('div[@class="p-name"]/a/text()').extract())
            price=self.check_list(site.xpath('div[@class="p-price"]/span/text()').extract())
            level_workshop_price=self.check_list(site.xpath('div[@class="p-price"]/strong/text()').extract())
            r = Request(sites_url ,meta={'sites_url':sites_url,'goods_id':goods_id,'goods_picture':goods_picture,'goods_name':goods_name,'price':price,'level_workshop_price':level_workshop_price} ,callback=self.parse_info)
            items.append(r)
        return items
    def parse_info(self,response):
        sel = Selector(response)
        item=OmtaoItem()

        titles = ['商品编码'.decode('utf-8'),'产地'.decode('utf-8'),'适用人群'.decode('utf-8'),'规格'.decode('utf-8')]
        detail={}

        root_type=self.check_list(sel.xpath('//div[@class="crumbs"]/a[2]/text()').extract())
        goods_brand_name=self.check_list(sel.xpath('//div[@class="crumbs"]/a[3]/text()').extract())
        goods_label=self.check_list(sel.xpath('//div[@id="product-intro"]/div[@id="intro"]/div/div[2]/p/text()').extract())
        good_reputation_rating=self.check_list(sel.xpath('//div[@id="product-intro"]/div[@id="intro"]/ul[@id="summary"]/li[@id="summary-evaluate"]/div[@class="dd"]/span/@title').extract())
        month_sale_number=self.check_list(sel.xpath('//li[@id="summary-evaluate"]/div[@class="dd"]/a/text()').extract())
        tariffs_detail=self.check_list(sel.xpath('//div[@id="product-intro"]/div[@id="intro"]/ul[@id="summary"]/li[@id="summary-logistic"]/div[@class="dd"]/div/em/text()').extract())
        product_detailsite=sel.xpath('//ul[@class="detail-list"]/li')
        for product_detail in product_detailsite:
            detailcontent=self.check_list(product_detail.xpath('text()').extract())
            title=detailcontent.split("：".decode('utf-8'),1)[0]
            content=detailcontent.split("：".decode('utf-8'),1)[1]
            if title in titles:
                detail[title]=content
        # data=self.check_list(product_detailsite.xpath('string(.)').extract()).strip()
        # product_detail1="".join(data.split('\t'))
        # product_detail2="".join(product_detail1.split('\n'))
        # product_detail="".join(product_detail2.split('\r'))
        item['goods_id'] = response.meta['goods_id']
        item['sites_url'] = response.meta['sites_url']
        item['goods_picture'] = response.meta['goods_picture']
        item['goods_name'] = response.meta['goods_name']
        item['price'] = response.meta['price']
        item['level_workshop_price'] = response.meta['level_workshop_price']
        item['root_type']=root_type
        item['goods_brand_name']=goods_brand_name
        item['goods_label']=goods_label
        item['good_reputation_rating']=good_reputation_rating
        item['month_sale_number']=month_sale_number
        item['tariffs_detail']=tariffs_detail

        item['goods_code']=self.getDictValue(detail,"商品编码")
        item['producting_area']=self.getDictValue(detail,"产地")
        item['for_peaple']=self.getDictValue(detail,"适用人群")
        item['goods_standard']=self.getDictValue(detail,"规格")
        return item

    def getDictValue(self,dict,param):
        if param.decode('utf-8'):
            return dict.get(param.decode('utf-8'),'')