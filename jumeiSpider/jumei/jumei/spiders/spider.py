# -*- coding: utf-8 -*-
from scrapy import Request
from jumei.items import JumeiItem
from scrapy.selector import Selector
from scrapy.spider import BaseSpider

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JumeiSpider(BaseSpider):
    name = "jumei"
    allowed_domains = ["jumei.com","jumeiglobal.com","koubei.jumei.com"]
    start_urls = [
        "http://item.jumeiglobal.com/ht151013p1584617t1.html?from=sr__6_10&site=sh"
    ]

    def check(self,jsonText,param):
        if param in jsonText:
            return jsonText[param]
        else:
            return ''

    def check2(self,dict,param):
        if param.decode('utf-8'):
            return dict.get(param.decode('utf-8'),'')

    def check3(self,list):
        if list:
            return list[0]
        else:
            return ''

    def extract(self , uncode_str,type):
        if len(uncode_str) > 8:
            return uncode_str[0]+uncode_str[-2:-1]
        if type == 'mall_product':
            return uncode_str[0:]
        else :
            return uncode_str[0:-1]

    #category list

    def parse(self,response):
        items=[]

        start_urls = [
            "http://search.jumei.com/?filter=0-11-1&cat=1&from=search_brother_category_1&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=3&from=search_brother_category_2&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=6&from=search_brother_category_3&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=21&from=search_brother_category_4&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=34&from=search_brother_category_5&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=77&from=search_brother_category_6&site=sh",
            "http://search.jumei.com/?filter=0-11-1&cat=417&from=search_brother_category_7&site=sh"

        ]

        for url in start_urls:
            r = Request(url,meta={'category_url':url},callback=self.parse_product_list)
            items.append(r)
        return items

    def parse_product_list(self,response):
        category_url = response.meta['category_url']
        sel = Selector(response)
        items = []

        next_page_url_list = sel.xpath('//div[@class="head_pagebtn"]/a[@class="enable next"]/@href').extract()
        if next_page_url_list:
            next_page_url = next_page_url_list[0]
            if next_page_url != '':
                r = Request(next_page_url , meta={'category_url':category_url},callback=self.parse_product_list)
                items.append(r)

        sites = [ sel.xpath('//li[@class="hai item"]'), sel.xpath('//li[@class="item"]'), sel.xpath('//li[@class="formall item"]')]

        for site in sites:
            for productSite in site:
                item = JumeiItem()
                pid = productSite.xpath('@pid').extract()
                bid = productSite.xpath('@bid').extract()
                cid = productSite.xpath('@cid').extract()
                product_type = productSite.xpath('@product_type').extract()[0]
                img_url = productSite.xpath('div/div/div/a/img/@src').extract()
                product_url = productSite.xpath('div/div/div[2]/a/@href').extract()[0]
                product_name_str = productSite.xpath('div/div/div[2]/a/text()').extract()
                if product_name_str[0].strip() =='':
                    product_name = product_name_str[1].strip()
                else:
                    product_name = product_name_str[0].strip()
                real_price = productSite.xpath('div/div/div[3]/div[2]/span/text()').extract()
                original_price_unicode = productSite.xpath('div/div/div[3]/div[2]/del/text()').extract()
                if original_price_unicode:
                    original_price = original_price_unicode[0][1:]
                else:
                    original_price = ''

                purchaserNumber_str = productSite.xpath('div/div/div[4]/div/text()').extract()
                if purchaserNumber_str[0].strip() =='':
                    purchaserNumber = purchaserNumber_str[1].strip()
                else:
                    purchaserNumber = purchaserNumber_str[0].strip()
                timeCountdown = productSite.xpath('div/div/div[4]/div[2]/@diff').extract()

                r = Request(product_url , meta={'category_url':category_url,'pid':pid,'real_price':real_price,'bid':bid,'cid':cid,
                      'product_type':product_type,'img_url':img_url,'product_url':product_url,'product_name':product_name,
                      'original_price':original_price,'purchaserNumber':purchaserNumber,'timeCountdown':timeCountdown} ,
                      callback=self.parse_detail)
                items.append(r)

        return items


    def parse_detail(self,response):
        #meta={'category':category,'detail_url':detail_url,'original_image':original_image,'jumei_price':jumei_price,'market_price':market_price}
        #category = response.meta['search_product_type']
        sel = Selector(response)
        items = []
        item = JumeiItem()
        titles = ['品牌'.decode('utf-8'),'功效'.decode('utf-8'), '生产地区'.decode('utf-8'),'适用人群'.decode('utf-8'), '产品规格'.decode('utf-8'),]
        detail={}

        #特卖
        if response.meta['product_type'] == 'deal':
            sites = sel.xpath('//div[@id="product_parameter"]/div[2]/textarea/table/tr')
            for site in sites:
                title = self.extract(site.select('td/b/text()').extract()[0],'deal')
                #print title
                content = self.check3(site.select('td[2]/span/text()').extract())
                #print content
                if title in titles:
                    detail[title] = content

        #极速免税
        if response.meta['product_type'] == 'global_deal' :
            sites = sel.xpath('//div[@class="deal_con_content"]/table/tbody/tr')
            for site in sites:
                title = self.extract(site.select('td/b/text()').extract()[0],'global_deal')
                content = self.check3(site.select('td[2]/span/text()').extract())
                if title in titles:
                    detail[title] = content

        #海外购
        if response.meta['product_type'] == 'global_mall':
            sites = sel.xpath('//div[@class="deal_con_content"]/table/tbody/tr')
            for site in sites:
                title = self.extract(site.select('td/b/text()').extract()[0],'global_deal')
                content = self.check3(site.select('td[2]/span/text()').extract())
                if title in titles:
                    detail[title] = content

        #普通商品
        if response.meta['product_type'] == 'mall_product':
            sites = sel.xpath('//div[@id="shoppingParameter"]/div/textarea/table/tbody/tr')
            for site in sites:
                title = self.extract(site.select('td/b/text()').extract()[0],'mall_product')
                content = self.check3(site.select('td[2]/span/text()').extract())
                if title in titles:
                    detail[title] = content

        #if response.meta['product_type'] == 'global_deal':
            #print response.meta['product_type']


        cid = response.meta['cid']
        category_url = response.meta['category_url']
        pid = response.meta['pid']
        bid = response.meta['bid']
        product_type = response.meta['product_type']
        product_name = response.meta['product_name']
        product_url = response.meta['product_url']
        original_price = response.meta['original_price']
        real_price = response.meta['real_price']
        purchaserNumber = response.meta['purchaserNumber']
        img_url = response.meta['img_url']
        timeCountdown = response.meta['timeCountdown']

        brand = self.check2(detail,"品牌")
        function = self.check2(detail,"功效")
        specification = self.check2(detail,"产品规格")
        forPeople = self.check2(detail,"适用人群")
        location = self.check2(detail,"生产地区")

        score_url = "http://koubei.jumei.com/comment_list-"+ response.meta['pid'][0] +"-1.html"
        r = Request(score_url , meta={'category_url':category_url,'pid':pid,'real_price':real_price,'bid':bid,'cid':cid,
                      'product_type':product_type,'img_url':img_url,'product_url':product_url,'product_name':product_name,
                      'original_price':original_price,'purchaserNumber':purchaserNumber,'timeCountdown':timeCountdown,
                       'brand': brand,'function':function,'forPeople':forPeople,'specification':specification,'location':location} ,
                    callback=self.parse_score)
        items.append(r)

        items.append(item)

        return items

    def parse_score(self,response):
        items=[]
        item=JumeiItem()
        item['avarage_rating']=response.xpath('//div[@class="rp_r_part_content"]/div[@class="rp_score white_scroes"]/span/text()').extract()[0].split("/")[0]
        rating_sites=[response.xpath('//div[@class="rp_r_part_content"]/dl[@class="rp_histogram"]') ]
        item['qingshuang_rating']=rating_sites[0].xpath('dt[1]/text()').extract()
        item['ziran_rating']=rating_sites[0].xpath('dt[2]/text()').extract()
        item['chijiu_rating']=rating_sites[0].xpath('dt[3]/text()').extract()
        item['zexia_rating']=rating_sites[0].xpath('dt[4]/text()').extract()

        part_sites=[response.xpath('//div[@class="rp_r_part_content"]/dl[@class="rp_histogram2 cl"]') ]
        item['skin_mix']=part_sites[0].xpath('dt[1]/text()').extract()
        item['skin_soul']=part_sites[0].xpath('dt[2]/text()').extract()
        item['skin_dry']=part_sites[0].xpath('dt[3]/text()').extract()
        item['skin_middle']=part_sites[0].xpath('dt[4]/text()').extract()
        item['skin_sensitive']=part_sites[0].xpath('dt[5]/text()').extract()

        item['categoryId'] = response.meta['cid']
        item['categoryUrl'] = response.meta['category_url']
        item['productId'] = response.meta['pid']
        item['brandId']= response.meta['bid']
        item['productType'] = response.meta['product_type']
        item['productName'] = response.meta['product_name']
        item['productUrl'] = response.meta['product_url']
        item['originalPrice'] = response.meta['original_price']
        item['realPrice'] = response.meta['real_price']
        item['purchaserNumber'] = response.meta['purchaserNumber']
        item['imageUrl'] = response.meta['img_url']
        item['timeCountdown'] = response.meta['timeCountdown']

        item['brand'] = response.meta['brand']
        item['function'] = response.meta['function']
        item['forPeople'] = response.meta['forPeople']
        item['specification'] = response.meta['specification']
        item['location'] = response.meta['location']

        items.append(item)

        return items