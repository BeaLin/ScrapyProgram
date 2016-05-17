# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
import urlparse
from ikjtao.items import IkjtaoItem
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class IkjtaoSpider(scrapy.spiders.Spider):
    name = 'kjtao'
    allowed_domains = ['ikjtao.com']
    start_urls = [
         "http://www.ikjtao.com/",
    ]

    def parse(self, response):
        sel = Selector(response)
        items = []
        #//input[contains(@id,'nt')]
        base_url = get_base_url(response)
        sites = sel.xpath('//li[@class=" j_CatNavItem cat-nav"]')
        for site in sites:
            item = IkjtaoItem()
            #一级目录
            supCategory = site.xpath('div/a/text()').extract()
            supCategoryUrl = [urlparse.urljoin(base_url,sub_url) for sub_url in site.xpath('div/a/@href').extract()]
            item['supCategory'] = self.checkListIsNull(supCategory)
            item['supCategoryUrl'] = self.checkListIsNull(supCategoryUrl)
            if item['supCategory'] != "热销产品".decode("utf-8"):
                request = scrapy.Request(item['supCategoryUrl'], callback = self.parseCategoryList)
                request.meta['item'] = item
                items.append(request)
        return items

    def parseCategoryList(self,response):
        itemMeta = response.meta['item']
        sel = Selector(response)
        items = []
        base_url = get_base_url(response)
        nextPageUrlList = sel.xpath('//a[@class="next"]/@href').extract()

        if nextPageUrlList:
            nextPageUrl = nextPageUrlList[0]
            if nextPageUrl != '':
                url_full = urlparse.urljoin(base_url,nextPageUrl)
                request = scrapy.Request(url_full,callback=self.parseCategoryList)
                request.meta['item'] = itemMeta
                items.append(request)

        sites = sel.xpath('//div[@class="item clearfix"]')
        for site in sites:
            item = IkjtaoItem()
            item['productName'] = self.checkListIsNull(site.xpath('p[2]/a/text()').extract())
            item['productUrl'] = self.checkListIsNull([urlparse.urljoin(base_url,sub_url) for sub_url in site.xpath('p[2]/a/@href').extract()])
            item['productId'] = self.checkListIsNull(re.findall(r'(\w*[0-9]+)\w*',item['productUrl']))
            item['productSalePrice'] = self.checkListIsNull(site.xpath('p/em/text()').extract())
            item['productMarketPrice'] = self.checkListIsNull(site.xpath('p/font/text()').extract())
            item['salesVolume'] = self.checkListIsNull(site.xpath('p[3]/span/em/text()').extract())
            item['commentNum'] = self.checkListIsNull(site.xpath('p[3]/span[2]/a/text()').extract())
            item['productImageUrl'] = self.checkListIsNull([urlparse.urljoin(base_url,sub_url) for sub_url in site.xpath('div/a/img/@src').extract()])

            item['supCategory'] = itemMeta['supCategory']
            item['supCategoryUrl'] = itemMeta['supCategoryUrl']
            request = scrapy.Request(item['productUrl'], callback = self.parseProductDetail)
            request.meta['item'] = item
            items.append(request)

        return items

    def parseProductDetail(self, response):
        itemMeta = response.meta['item']
        sel = Selector(response)
        items = []
        titles = ['品牌'.decode('utf-8'),'产地'.decode('utf-8'), '成分'.decode('utf-8'),
                  '用途'.decode('utf-8'), '商品货号'.decode('utf-8'),'商品品牌'.decode('utf-8'),'商品重量'.decode('utf-8'),
                  '商品税率'.decode('utf-8'),'货品标签'.decode('utf-8')]
        item = IkjtaoItem()

        detail = {}

        for site in sel.xpath('//ul[@class="inLeft_attributes"]/li'):
            title_original = self.checkListIsNull(site.xpath('text()').extract())
            content = self.checkListIsNull(site.xpath('span/text()').extract())
            if len(content) != 0 :
                title_real = title_original.split("：".decode('utf-8'),1)[0]
                content_real = content
            else :
                title_real = title_original.split("：".decode('utf-8'),1)[0]
                content_real = title_original.split("：".decode('utf-8'),1)[1]
                if content_real == '':
                    content_real = self.checkListIsNull(site.xpath('a/text()').extract())
            if title_real in titles:
                detail[title_real] = content_real

        item['monthlySales'] = self.checkListIsNull(sel.xpath('//li[@class="tm-ind-item tm-ind-sellCount"]/p[1]/text()').extract())
        item['brand'] = self.getDictValue(detail,"品牌")
        item['location'] = self.getDictValue(detail,"产地")
        item['composition'] = self.getDictValue(detail,"成分")
        item['application'] = self.getDictValue(detail,"用途")
        item['itemNo'] = self.getDictValue(detail,"商品货号")
        item['commodityBrand'] = self.getDictValue(detail,"商品品牌")
        item['weight'] = self.getDictValue(detail,"商品重量")
        item['taxRate'] = self.getDictValue(detail,"商品税率")
        item['tag'] = self.getDictValue(detail,"货品标签")

        item['supCategory'] = itemMeta['supCategory']
        item['supCategoryUrl'] = itemMeta['supCategoryUrl']

        item['productName'] = itemMeta['productName']
        item['productId'] = itemMeta['productId']
        item['productUrl'] = itemMeta['productUrl']
        item['productSalePrice'] = itemMeta['productSalePrice']
        item['productMarketPrice'] = itemMeta['productMarketPrice']
        item['salesVolume'] = itemMeta['salesVolume']
        item['commentNum'] = itemMeta['commentNum']
        item['productImageUrl'] = itemMeta['productImageUrl']

        items.append(item)

        return items

    def checkListIsNull(self,list):
        if list:
            return list[0].strip()
        else:
            return ''

    def getDictValue(self,dict,param):
        if param.decode('utf-8'):
            return dict.get(param.decode('utf-8'),'')