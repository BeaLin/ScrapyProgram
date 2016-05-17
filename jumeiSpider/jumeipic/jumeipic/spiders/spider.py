from scrapy.spiders import Spider
from jumeipic.items import JumeipicItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy import Request
import json

class PictureSpider(Spider):
    name = "jumeipic"
    allowed_domains = ["h5.jumei.com","omtao.com"]
    start_urls = [
		"http://h5.jumei.com/mall/index?type=category"
    ]
    def check(self,jsonText,param):
        if param in jsonText:
            return jsonText[param]
        else:
            return ''
        
    def parse(self, response):
        items=[]
        for sel in response.xpath('//div[@class="mall-content"]'):
            for cat in sel.xpath('//div[@class="mall-deal-route-item-area clearfloat"]/span/a/text()').extract():
                url = "http://h5.jumei.com/mall/ajaxList/?type=category&page=1&search="+cat
                r= Request(url,callback=self.parse_pic)
                items.append(r)
                print url
        return items
        
    def parse_pic(self,response):
        jsonresponses = json.loads(response.body_as_unicode())
        items = []
        images=[]
        base_url=get_base_url(response)
        cat=base_url.split("search=")[1]
        
        page_unicode = jsonresponses['page']
        totalPage_unicode = jsonresponses['page_count']

        next_page_num = int(page_unicode) + 1
        totalPage_num = int(totalPage_unicode)
        next_page_str = str(next_page_num)

        next_list = "http://h5.jumei.com/mall/ajaxList/?type=category&page="+next_page_str+"&search="+cat
        if next_page_num<=totalPage_num:
            url = next_list
            r = Request(url, callback=self.parse_pic)
            items.append(r)

        print "next_list:" + next_list
        
        for jsonresponse in jsonresponses['item_list']:
            images.append(jsonresponse['original_image'])
        item = JumeipicItem()
        item['image_urls']=[urljoin_rfc(base_url,ru) for ru in images]
        items.append(item)

        return items
    
