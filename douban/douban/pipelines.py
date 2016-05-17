# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DoubanPipeline(object):
    def __init__(self):
        filename="E:/WorkSpace/DataCrawl/DoubanReview/doubanReview.json"
        self.file=codecs.open(filename,'w',encoding='utf-8')
    def process_item(self, item, spider):
        line =json.dumps(dict(item))+'\n'
        self.file.write(line.decode('unicode_escape'))
        return item
