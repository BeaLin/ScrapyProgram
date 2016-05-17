# -*- coding: utf-8 -*-
import datetime
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy.utils.response import get_base_url

from tutorial.items import miaItem
import string

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DmozSpider(Spider):
    name = "mia"
    allowed_domains = ["mia.com"]
    start_urls = ["http://www.mia.com/"]

    def checkListIsNull(self,list):
        if list:
            return list[0].strip()
        else:
            return ''
    def getListInfo(self,list):
        if list:
            return list[1].strip()
        else:
            return ''
    def check_dict(self,dict,param):
        if param.decode('utf-8'):
            return dict.get(param.decode('utf-8'),'')


    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="l right CateCon"]/div[@class="tcate"]')
        items = []
        #获取所有分类的URL
        for site in sites:
            ccon_sites = [site.xpath('div[@class="ccon"]'), site.xpath('div[@class="ccon pb0"]')]
            for ccon_site in ccon_sites:
                for a_sites in ccon_site:
                    a_sites=a_sites.xpath('a')
                    for url_site in a_sites:
                        next_page_url=self.checkListIsNull(url_site.xpath('@href').extract())
                        r = Request(next_page_url, callback=self.parse_product)
                        items.append(r)
        return items

    def parse_product(self, response):
        items=[]
        sel = Selector(response)

        #获取当前页面的相关信息
        page_url_list = sel.xpath('//div[@class="Lcon content clearfix"]/div[@class="block"]')
        for page_url in page_url_list:
            level_workshop_price=self.checkListIsNull(page_url.xpath('div[@class="bmfo"]/div[@class="saled"]/div/'
                                                                     'span[@class="Tahoma f20 pink"]/text()').extract())
            price=self.checkListIsNull(page_url.xpath('div[@class="bmfo"]/div[@class="saled"]/div/span[@class="originalPrice"]/text()').extract())
            next_page_url_short=self.checkListIsNull(page_url.xpath('a/@href').extract())
            next_page_url='http://www.mia.com'+next_page_url_short
            r = Request(next_page_url,meta={'level_workshop_price':level_workshop_price,
                                            'price':price},callback=self.parse_product_detail)
            items.append(r)

        #判断是否有分页
        isends=[]
        isend_urls=sel.xpath('//div[@class="right l"]/div[@class="Lpage page tr"]/p/a')
        for isend_url in isend_urls:
            isend=isend_url.xpath('text()').extract()
            isends.append(isend)
        #isends为空表示无分页，不为空表示有分页
        if isends:
             #判断当前页是否是最后一页，如果不是，则构建下一个页的URL
             if isends[-1][-1]=='>'.decode('utf-8'):
                 next_page_url_short=self.checkListIsNull(sel.xpath('//div[@class="right l"]/div[@class="Lpage page tr"]/p/a[1]/@href').extract())
                 item=miaItem()
                 base_url=get_base_url(response)
                 contains = base_url.count('per_page=') > 0
                 if contains:
                     next_page_url_short_number='%d'%(int(base_url.split('per_page=')[1])+40)
                 else:
                     next_page_url_short_number='%d'%40
                 next_page_url_page='http://www.mia.com'+next_page_url_short.split('per_page=')[0]+'per_page='+next_page_url_short_number

                 #将下一页的URL进行回调
                 r = Request(next_page_url_page,callback=self.parse_product)
                 items.append(r)
        return items

    def parse_product_detail(self,response):
        sel = Selector(response)
        items = []
        site = sel.xpath(
            '//div[@class="introduction clearfix"]/div[1]/div[2]/div[@class="datacon area0 clearfix cs rel"]/ul[@class="clearfix"]')
        titles_area = '产地:'.decode('utf-8')
        titles_article_number = '编码：'.decode('utf-8')
        titles_tax_rate = '关税：'.decode('utf-8')
        titles_weight = '规格尺寸:'.decode('utf-8')
        titles_use_age = '适用年龄:'.decode('utf-8')
        item = miaItem()
        goods_name = self.checkListIsNull(site.xpath('li[1]/text()').extract())
        goods_brand_name = self.checkListIsNull(site.xpath('li[2]/text()').extract())
        child_type = self.checkListIsNull(site.xpath('li[3]/text()').extract())
        mia_viewpoint=self.checkListIsNull(site.xpath('//div[@class="pointOfView clearfix"]/div/p/text()').extract())
        weight_label0 = self.checkListIsNull(site.xpath('li[5]/b/text()').extract())
        weight_label1 = self.checkListIsNull(site.xpath('li[6]/b/text()').extract())
        weight_info0 = self.checkListIsNull(site.xpath('li[5]/text()').extract())
        weight_info1 = self.checkListIsNull(site.xpath('li[6]/text()').extract())
        if weight_label0 in titles_weight:
            item['weight'] = weight_info0
        if weight_label1 in titles_weight:
            item['weight'] = weight_info1
        else:
            item['weight'] =''
        producting_area_label2 = self.checkListIsNull(site.xpath('li[6]/b/text()').extract())
        producting_area_actual2 = self.checkListIsNull(site.xpath('li[6]/text()').extract())
        producting_area_label0 = self.checkListIsNull(site.xpath('li[7]/b/text()').extract())
        producting_area_label1 = self.checkListIsNull(site.xpath('li[8]/b/text()').extract())
        producting_area_actual0 = self.checkListIsNull(site.xpath('li[7]/text()').extract())
        producting_area_actual1 = self.checkListIsNull(site.xpath('li[8]/text()').extract())
        if producting_area_label0 == titles_area:
            item['producting_area'] = producting_area_actual0
        if producting_area_label1 == titles_area:
            item['producting_area'] = producting_area_actual1
        if producting_area_label2 == titles_area:
            item['producting_area'] = producting_area_actual2
        else:
            item['producting_area'] =''
        if producting_area_label0 == titles_use_age:
            item['use_age'] = producting_area_actual0
        if producting_area_label1 == titles_use_age:
            item['use_age'] = producting_area_actual1
        if producting_area_label2 == titles_use_age:
            item['use_age'] = producting_area_actual2
        if weight_label1 in titles_use_age:
            item['use_age'] = weight_info1
        if weight_label0 in titles_use_age:
            item['use_age'] = weight_info0
        else:
            item['use_age'] =''
        goods_label = self.getListInfo(sel.xpath('//div[@class="left yahei l"]/text()').extract())
        good_reputation_rating = self.checkListIsNull(sel.xpath('//div[@class="pi_attr_box"]/div[2]/'
                                                                'dl[1]/dd/em/text()').extract())
        details_urls = sel.xpath('//div[@class="pi_attr_box"]/dl[@class="other"]')

        '''
        comment_urls=sel.xpath('//div[@class="area2 clearfix wordOfMouth datacon"]/div[@class="pblock clearfix"]')
        for comment_url in comment_urls:
            item['user_type']=self.checkListIsNull(comment_url.xpath('div[1]/div[1]/img/text()').extract())
            item['comments_title']=self.checkListIsNull(comment_url.xpath('div[1]/div[2]/h4/span/text()').extract())
            item['comments_content']=self.checkListIsNull(comment_url.xpath('div[1]/div[2]/p/text()').extract())
            img_urls=comment_url.xpath('div[1]/div[2]/div[@clss="groupimg clearfix"]/img/')
            img_str=''
            for img_url in img_urls:
                img_info=self.checkListIsNull(img_url.xpath('text()').extract())
                img_str+=img_info+'     '
            item['comments_imgs']=img_str
        '''
        for details_url in details_urls:
            tax_str=''
            label=self.checkListIsNull(details_url.xpath('dt/text()').extract())
            info=self.checkListIsNull(details_url.xpath('dd/text()').extract())
            if label == titles_article_number:
                item['article_number'] = info
            else:
                item['article_number'] = ''
            if label == titles_tax_rate:
                tax_str = info
            item['tax_rate'] = tax_str
        base_url=get_base_url(response)
        item['goods_url']=base_url
        price = self.checkListIsNull(sel.xpath('//div[@class="pi_price_box"]/span[1]/em/text()').extract())
        level_workshop_price = self.checkListIsNull(
            sel.xpath('//div[@class="pi_price_box"]/span[3]/del/text()').extract())
        goods_picture= self.checkListIsNull(
            sel.xpath('//div[@class="left l rel"]/div[@class="big rel"]/img/@src').extract())
        item['goods_picture']=goods_picture
        str=''
        for divs in sel.xpath('//div[@class="area1 clearfix datacon"]/img'):
            img_url=self.checkListIsNull(divs.xpath('@data-src').extract())
            str+=img_url+'  '
        item['images_urls'] =str
        item['goods_brand_name'] = goods_brand_name
        item['child_type'] = child_type
        item['goods_name'] = goods_name
        item['goods_label'] = goods_label
        item['good_reputation_rating'] = good_reputation_rating
        item['level_workshop_price'] = level_workshop_price
        item['price'] = price
        item['mia_viewpoint']=mia_viewpoint
        items.append(item)
        return items







