# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import datetime

class JumeiPipeline(object):

    def __init__(self):
        today = datetime.date.today().strftime("%Y%m%d")
        self.file = codecs.open(today+'product.json','w',encoding='GB18030')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))+ '\n'
        self.file.write(line.decode('unicode_escape'))
        return item