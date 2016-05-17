# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import codecs
import json

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy import log


class TutorialPipeline(object):
    def __init__(self):
        today = datetime.date.today().strftime("%Y%m%d")
        str='/home/ideas/CrawlData/'+today +'_mias_info.json'
        #str='E:\javacode\myScraoyData'+today+'_mia_info.json'
        self.file = codecs.open(str,'w',encoding='utf-8')

    #pipeline默认调用
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+ '\n'
        self.file.write(line.decode('unicode_escape'))
        return item

class tutorialPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '10.82.80.7',
            db ='Spider_haitao',
            user = 'root',
            passwd = '123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False)

    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    #将每行写入数据库中
    def _conditional_insert(self, tx, item):
        today = datetime.date.today().strftime("%Y%m%d")
        sql = "create table if not exists mias" + today + \
              """(goods_id INT(100) PRIMARY KEY NOT NULL AUTO_INCREMENT,
              goods_name VARCHAR(50) DEFAULT NULL,
              goods_label VARCHAR(5000) DEFAULT NULL,
              good_reputation_rating VARCHAR(20) DEFAULT NULL,
              level_workshop_price VARCHAR(80) DEFAULT NULL,
              price VARCHAR(80) DEFAULT NULL,
              mia_viewpoint VARCHAR(5000) DEFAULT NULL,
              weight VARCHAR(80) DEFAULT NULL,
              tax_rate VARCHAR(50) DEFAULT NULL,
              use_age VARCHAR(50) DEFAULT NULL,
              goods_brand_name VARCHAR(50) DEFAULT NULL,
              child_type VARCHAR(50) DEFAULT NULL,
              producting_area VARCHAR(20) DEFAULT NULL,
              article_number VARCHAR(50) DEFAULT NULL,
              crawling_time VARCHAR(50) DEFAULT NULL,
              goods_url VARCHAR(100) DEFAULT NULL,
              goods_picture VARCHAR(100) DEFAULT NULL,
              images_urls VARCHAR(8000) DEFAULT NULL
              )ENGINE=INNODB DEFAULT CHARSET=utf8"""
        tx.execute(sql)
        tx.execute("insert into mias"+today +"(goods_name,goods_label,good_reputation_rating,level_workshop_price,price,mia_viewpoint,"
                                           "weight,tax_rate,use_age,goods_brand_name,"
                                           "child_type,producting_area,article_number,crawling_time,goods_url,goods_picture,images_urls) values (%s,%s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)",
                           (item['goods_name'], item['goods_label'], item['good_reputation_rating'], item['level_workshop_price'], item['price'],
                            item['mia_viewpoint'],item['weight'], item['tax_rate'], item['use_age'], item['goods_brand_name'],
                            item['child_type'],item['producting_area'],item['article_number'],datetime.datetime.now(),item['goods_url'],item['goods_picture'],item['images_urls']))
    def handle_error(self,e):
        log.err(e)

