from scrapy.spiders import Spider
from picture.items import PictureItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy import Request
import json

class PictureSpider(Spider):
    name = "lefeng"
    allowed_domains = ["m.lefeng.com"]
    start_urls = [
		"http://m.lefeng.com/index.php/widget/get_product_list?aid=-x-equ-html5-&output=json&sortId=0&brandId=0&param=2&pageNo=607&spec=&price="
    ]

    def parse(self, response):
        jsonresponses = json.loads(response.body_as_unicode())
        items = []
        images=[]

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

        item = PictureItem()
        for jsonresponse in jsonresponses['data'][0]['items']:
            images.append(jsonresponse['img_260'])
        base_url = get_base_url(response)
        item['image_urls'] = [urljoin_rfc(base_url,ru) for ru in images]
        items.append(item)
        return items
