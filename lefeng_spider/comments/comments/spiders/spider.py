from scrapy.spiders import Spider
from comments.items import CommentsItem
import json
from scrapy import Request

class CommentsSpider(Spider):
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
            url = "http://m.lefeng.com/index.php/widget/product_comment/pid/"+jsonresponse['productId']+"?aid=-x-equ-html5-&output=json&pageno=1"
            r = Request(url,meta={'productId':jsonresponse['productId']} ,callback=self.parse_comment)
            items.append(r)
        return items

    def parse_comment(self,response):
        productId=response.meta['productId']
        productId_str = productId.encode("utf-8")
        jsonresponses = json.loads(response.body_as_unicode())
        items = []
        if len(jsonresponses['data'][0]):
            print jsonresponses['data']
            page_unicode = jsonresponses['data'][0]['pageNo']
            totalPage_unicode = jsonresponses['data'][0]['totalPages']
            page_str = page_unicode.encode("utf-8")
            totalPage_str = totalPage_unicode.encode("utf-8")
            next_page_num = int(page_str.strip()) + 1
            totalPage_num = int(totalPage_str)
            next_page_str = str(next_page_num)

            next_list = "http://m.lefeng.com/index.php/widget/product_comment/pid/"+productId_str+"?aid=-x-equ-html5-&output=json&pageno="+next_page_str+""

            if next_page_num<=totalPage_num:
                url = next_list
                r = Request(url,meta={'productId':productId_str},callback=self.parse_comment)
                items.append(r)

            print "comment_page" + next_list

            for jsonresponse in jsonresponses['data'][0]['result']:
                item = CommentsItem()
                item['createdAt']=jsonresponse['createdAt']
                item['id']=jsonresponse['id']
                item['productId']=jsonresponse['productId']
                item['productScore']=jsonresponse['productScore']
                item['remark']=jsonresponse['remark']
                item['reply']=jsonresponse['reply']
                item['type']=jsonresponse['type']
                item['userId']=jsonresponse['userId']
                item['userName']=jsonresponse['userName']

                items.append(item)

        return items