# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import codecs
import json
import datetime
import time
import MySQLdb.cursors
import MySQLdb
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class SQLStorePipeline(object):
    def __init__(self):
        self.dbpool=adbapi.ConnectionPool('MySQLdb',host = '10.82.80.7' , db = 'Spider_haitao' ,
                    user='root', passwd = '123456' , cursorclass=MySQLdb.cursors.DictCursor, charset='utf8', use_unicode=True)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx , item):
        today = datetime.date.today().strftime("%Y%m%d")
        sql = "create table if not exists oumeitao" + today + \
              """(goods_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
              goods_name VARCHAR(100) DEFAULT NULL,
              goods_url VARCHAR(100) DEFAULT NULL,
              goods_picture_url VARCHAR(100) DEFAULT NULL,
              sale_price VARCHAR(20) DEFAULT NULL,
              market_price VARCHAR(20) DEFAULT NULL,
              month_sales VARCHAR(20) DEFAULT NULL,
              sup_category VARCHAR(50) DEFAULT NULL,
              brand VARCHAR(100) DEFAULT NULL,
              location VARCHAR(100) DEFAULT NULL,
              goods_standard VARCHAR(50) DEFAULT NULL,
              goods_label VARCHAR(200) DEFAULT NULL,
              good_reputation_rating VARCHAR(50) DEFAULT NULL,
              tariffs_detail VARCHAR(50) DEFAULT NULL,
              for_peaple VARCHAR(50) DEFAULT NULL,
              goods_code VARCHAR(50) DEFAULT NULL,
              crawl_site VARCHAR(10) DEFAULT NULL,
              crawling_time DATETIME DEFAULT NULL
              )ENGINE=INNODB DEFAULT CHARSET=utf8"""

        tx.execute(sql)
        tx.execute(
            "insert into oumeitao"+ today +" (goods_name,goods_url,goods_picture_url,sale_price,market_price,"
                                         "month_sales,sup_category,brand,location,goods_standard,goods_label,good_reputation_rating,"
                                         "tariffs_detail,for_peaple,goods_code,crawl_site,crawling_time"
                                         " )\
             values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s)",
            (item['goods_name'],item['sites_url'],item['goods_picture'],item['level_workshop_price'],item['price'],item['month_sale_number'],
             item['root_type'],item['goods_brand_name'],item['producting_area'],item['goods_standard'],item['goods_label'],
             item['good_reputation_rating'],item['tariffs_detail'],item['for_peaple'],item['goods_code'],"欧美淘".decode('utf-8'),datetime.datetime.now())
        )
        #log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self,e):
        log.err(e)


class OmtaoPipeline(object):
    def __init__(self):
        datefilename="/home/ideas/CrawlData/"+time.strftime("%Y%m%d")+"_omtao_info.json"
        #datefilename="E:/WorkSpace/DataCrawl/"+time.strftime("%Y%m%d")+"_omtao_info.json"
        self.file=codecs.open(datefilename,'w',encoding='utf-8')

    def process_item(self, item, spider):
        line =json.dumps(dict(item))+'\n'
        self.file.write(line.decode('unicode_escape'))
        return item
