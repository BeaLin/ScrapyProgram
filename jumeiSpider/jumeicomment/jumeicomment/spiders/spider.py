from scrapy.spiders import Spider
from jumeicomment.items import JumeicommentItem
from scrapy.selector import Selector
from scrapy import Request

class CommentsSpider(Spider):
    name = "jumeicomment"
    allowed_domains = ["koubei.jumei.com"]
    start_urls = [
		"http://koubei.jumei.com/product_categories.html"
    ]
    def check_list(self,list):
        if list:
            return list[0]
        else:
            return ''

    def parse(self,response):
        items=[]
        sites=response.xpath('//div[@class="brand_classify"]')
        for site in sites:
            brand_sites=site.xpath('div[@class="l br_center"]/a')
            for brand_site in brand_sites:
                brand_url="http://koubei.jumei.com"+self.check_list(brand_site.xpath('@href').extract())
                r = Request(brand_url ,callback=self.parse_brand)
                items.append(r)                      
        return items

    def parse_brand(self,response):
        sel = Selector(response)
        items=[]
        product_sites=sel.xpath('//div[@class="product_result_box"]/ul/li')
        for product_site in product_sites:
            img_src=self.check_list(product_site.xpath('a[@class="pro_item"]/img/@src').extract())
            if img_src=='':
                product_id=''
            else:
                img_id=img_src.split('/')[-1]
                product_id=img_id.split('_')[0]
            
            product_name=self.check_list(product_site.xpath('div[@class="searchlist_tit"]/a/text()').extract())
            comment_href=self.check_list(product_site.xpath('a[@class="pro_item"]/@href').extract())
            comment_temp=comment_href.split('_')[-1]
            comment_id=comment_temp.split(".")[0]
            comment_url="http://koubei.jumei.com/comment_list-"+comment_id+"-1.html"
            r = Request(comment_url ,meta={'product_id':product_id,'product_name':product_name} ,callback=self.parse_comment)
            items.append(r)
        next_brandpage=response.xpath('//div[@class="pageSplit"]/a[@class="next"]/@href').extract()
        if len(next_brandpage):
            next_brandpage_url="http://koubei.jumei.com"+next_brandpage[0]
            r = Request(next_brandpage_url ,callback=self.parse_brand)
            items.append(r)
        return items

    def parse_comment(self,response):
        items=[]
        productId = response.meta['product_id']
        productName=response.meta['product_name']
        comment_sites=response.xpath('//li[@class="pfTrends"]')
        for comment_site in comment_sites:
            item=JumeicommentItem()
            item['product_id'] = productId
            item['product_name']=productName
            item['user_name']=self.check_list(comment_site.xpath('div[@class="report"]/div[@class="user_info"]/span[@class="user_name"]/a/text()').extract())
            item['user_detail']=self.check_list(comment_site.xpath('div[@class="report"]/div[@class="user_info"]/span[@class="user_attr"]/text()').extract())
            item['user_comment']=self.check_list(comment_site.xpath('div[@class="report"]/div[@class="report_content"]/div/text()').extract())
            item['comment_time']=self.check_list(comment_site.xpath('div[@class="report_time"]/text()').extract())
            items.append(item)
        
        next_page=response.xpath('//div[@class="pageSplit"]/a[@class="next"]/@href').extract()
        if len(next_page):
            next_page_url="http://koubei.jumei.com/"+next_page[0]
            r = Request(next_page_url ,meta={'product_id':productId,'product_name':productName},callback=self.parse_comment)
            items.append(r)
        return items