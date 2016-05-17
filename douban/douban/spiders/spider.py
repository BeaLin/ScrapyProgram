# -*- coding: utf-8 -*-
from douban.items import DoubanItem
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
import json
#import codecs
#codecs.register(lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None)

class DoubanSpider(Spider):
    name = "douban"
    allowed_domains = ["book.douban.com","www.douban.com"]
    start_urls = [
        "https://book.douban.com/top250?start=0",
        "https://book.douban.com/top250?start=25",
        "https://book.douban.com/top250?start=50",
        "https://book.douban.com/top250?start=75",
        "https://book.douban.com/top250?start=100",
        "https://book.douban.com/top250?start=125",
        "https://book.douban.com/top250?start=150",
        "https://book.douban.com/top250?start=175",
        "https://book.douban.com/top250?start=200",
        "https://book.douban.com/top250?start=225"
    ]
    def check_list(self,list):
        if list:
            return list[0]
        else:
            return ''

    def parse(self, response):
        items=[]
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        urlsites=response.xpath('//div[@class="indent"]/table')
        for urlsite in urlsites:
            book_url=self.check_list(urlsite.xpath('tr/td[2]/div[@class="pl2"]/a/@href').extract())
            #print("book_url")
            #print book_url
            book_name=self.check_list(urlsite.xpath('tr/td[2]/div[@class="pl2"]/a/text()').extract()).strip()
            #print("book_name")
            #print book_name
            book_authorall=self.check_list(urlsite.xpath('tr/td[2]/p[@class="pl"]/text()').extract())
            book_author=book_authorall.split("/")[0]
            #print("book_author:")
            #print book_author
            review_url=book_url+"reviews"
            r = Request(review_url ,meta={'book_url':book_url,'book_name':book_name,'book_author':book_author} ,callback=self.parse_info)
            items.append(r)
        return items

    def parse_info(self,response):
        items=[]
        sel = Selector(response)
        book_url=response.meta['book_url']
        book_name=response.meta['book_name']
        book_author=response.meta['book_author']
        review_sites=sel.xpath('//div[@class="ctsh"]')
        for review_site in review_sites:
            review_full=self.check_list(review_site.xpath('div[@class="tlst"]/div[@class="nlst"]/h3/div/@id').extract())
            review_full_url="https://book.douban.com/j/review/"+review_full.split("-")[1]+"/fullinfo"
            review_author=self.check_list(review_site.xpath('div[@class="tlst"]/div[@class="clst"]/span/span[@class="starb"]/a/text()').extract())
            review_score=self.check_list(review_site.xpath('div[@class="tlst"]/div[@class="clst"]/span/span[2]/@title').extract())
            r= Request(review_full_url,meta={'book_url':book_url,'book_name':book_name,'book_author':book_author,'review_author':review_author,'review_score':review_score},callback=self.parse_review)
            items.append(r)

        next_review=response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if len(next_review):
            r = Request(next_review[0] ,meta={'book_url':book_url,'book_name':book_name,'book_author':book_author} ,callback=self.parse_info)
            items.append(r)
        return items
    def parse_review(self,response):
        jsonresponses = json.loads(response.body_as_unicode())
        item=DoubanItem()
        review=jsonresponses['html']
        item['book_name']=response.meta['book_name']
        item['book_url']=response.meta['book_url']
        item['book_author']=response.meta['book_author']
        item['review_author']=response.meta['review_author']
        item['review_score']=response.meta['review_score']
        item['review']=review.split("<div class")[0]
        return item
