from scrapy.spiders import Spider
from products.items import ProductsItem
import json
from scrapy import Request

class LefengSpider(Spider):
    name = "lefeng"
    allowed_domains = ["m.lefeng.com"]
    start_urls = [
		"http://m.lefeng.com/index.php/widget/get_product_list?aid=-x-equ-html5-&output=json&sortId=0&brandId=0&param=2&pageNo=1&spec=&price="
    ]

    def check(self,jsonText,param):
        if param in jsonText:
            return jsonText[param]
        else:
            return ''

    def parse(self,response):
        jsonresponses = json.loads(response.body_as_unicode())
        items = []

        page_unicode = jsonresponses['data'][0]['pageNo']
        totalPage_unicode = jsonresponses['data'][0]['totalPage']
        page_str = page_unicode.encode("utf-8")
        totalPage_str = totalPage_unicode.encode("utf-8")
        #print type(page_str)
        next_page_num = int(page_str.strip()) + 1
        totalPage_num = int(totalPage_str)
        next_page_str = str(next_page_num)

        next_list = "http://m.lefeng.com/index.php/widget/get_product_list?aid=-x-equ-html5-&output=json&sortId=0&brandId=0&param=2&pageNo="+next_page_str+"&spec=&price="

        if next_page_num<=totalPage_num:
            url = next_list
            r = Request(url, callback=self.parse)
            items.append(r)

        print "next_list:" + next_list

        for jsonresponse in jsonresponses['data'][0]['items']:
            item = ProductsItem()
            item['brandId'] = self.check(jsonresponse,'brandId')
            item['brandName'] = self.check(jsonresponse,'brandName')
            item['brandUrl'] = self.check(jsonresponse,'brandUrl')
            item['commentNumber']=self.check(jsonresponse,'commentNumber')
            item['imgUrl']=self.check(jsonresponse,'imgUrl')
            item['marketPrice']=self.check(jsonresponse,'marketPrice')
            item['productName']=self.check(jsonresponse,'productName')
            item['productId']=self.check(jsonresponse,'productId')
            item['salePrice']=self.check(jsonresponse,'salePrice')

            items.append(item)


        return items