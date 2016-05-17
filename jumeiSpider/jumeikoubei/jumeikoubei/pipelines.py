# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import time

class JumeikoubeiPipeline(object):
    def __init__(self):
        datefilename="d:/datacrawl/"+time.strftime("%Y%m%d")+"_koubei.json"
        self.file=codecs.open(datefilename,'w',encoding='utf-8')
        
    def process_item(self, item, spider):
        line =json.dumps(dict(item))+'\n'
        self.file.write(line.decode('unicode_escape'))
        return item