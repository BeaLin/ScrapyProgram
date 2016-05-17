from scrapy.spiders import Spider
from jumeiscore.items import JumeiscoreItem
from scrapy.selector import Selector
from scrapy import Request

class ScoreSpider(Spider):
    name = "jumeiscore"
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
            r = Request(comment_url ,meta={'product_id':product_id,'product_name':product_name} ,callback=self.parse_score)
            items.append(r)
        next_brandpage=response.xpath('//div[@class="pageSplit"]/a[@class="next"]/@href').extract()
        if len(next_brandpage):
            next_brandpage_url="http://koubei.jumei.com"+next_brandpage[0]
            r = Request(next_brandpage_url ,callback=self.parse_brand)
            items.append(r)
        return items

    def parse_score(self,response):
        items=[]
        item=JumeiscoreItem()
        item['product_id'] = response.meta['product_id']
        item['product_name']=response.meta['product_name']
        item['avarage_rating']=self.check_list(response.xpath('//div[@class="rp_r_part_content"]/div[@class="rp_score white_scroes"]/span/text()').extract()).split("/")[0]
        detail_sites=response.xpath('//div[@class="rp_r_part_content"]/dl[@class="rp_histogram"]/dd')
        score_sites=response.xpath('//div[@class="rp_r_part_content"]/dl[@class="rp_histogram"]/dt')
        score=''
        i=0
        for detail_site in detail_sites:
            detail=self.check_list(detail_site.xpath('span/span[@class="txt"]/text()').extract())
            detail_score=self.check_list(score_sites[i].xpath('text()').extract())
            score=score+";"+detail+":"+detail_score
            i=i+1
        item['detail_score']=score
        part=''
        part_sites=response.xpath('//div[@class="rp_r_part_content"]/dl[@class="rp_histogram2 cl"]/dt')
        for part_site in part_sites:
            part=part+";"+part_site.xpath('text()').extract()[0]    
        item['skin_part']=part
        item['koubei_count']=self.check_list(response.xpath('//div[@class="score_des"]/a[1]/text()').extract())
        item['comment_count']=self.check_list(response.xpath('//div[@class="score_des"]/a[2]/text()').extract())
        items.append(item)
                         
        return items

