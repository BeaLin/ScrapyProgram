# -*- coding: utf-8 -*-

import codecs
import json
import datetime

from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb
# from scrapy import log
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format = ('%(levelname)s: %(message)s'),
    level = logging.DEBUG
)
logger = logging.getLogger('mycustomerlogger')

class SQLStorePipeline(object):
    def __init__(self):

        self.dbpool = adbapi.ConnectionPool('MySQLdb',host = '10.82.80.7' , db = 'Spider_haitao' ,
                    user='root', passwd = '123456' , cursorclass=MySQLdb.cursors.DictCursor, charset='utf8', use_unicode=True)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx , item):
        today = datetime.date.today().strftime("%Y%m%d")

        sql = "create table if not exists ikjtao" + today + \
              """(goods_id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
              goods_name VARCHAR(50) DEFAULT NULL,
              goods_url VARCHAR(100) DEFAULT NULL,
              goods_picture_url VARCHAR(100) DEFAULT NULL,
              sale_price VARCHAR(20) DEFAULT NULL,
              market_price VARCHAR(20) DEFAULT NULL,
              sales_volume VARCHAR(20) DEFAULT NULL,
              comment_num VARCHAR(20) DEFAULT NULL,
              sup_category VARCHAR(50) DEFAULT NULL,
              sup_category_url VARCHAR(100) DEFAULT NULL,
              month_sales VARCHAR(20) DEFAULT NULL,
              brand VARCHAR(100) DEFAULT NULL,
              location VARCHAR(100) DEFAULT NULL,
              composition VARCHAR(100) DEFAULT NULL,
              application VARCHAR(50) DEFAULT NULL,
              item_no VARCHAR(30) DEFAULT NULL,
              commodity_brand VARCHAR(100) DEFAULT NULL,
              weight VARCHAR(20) DEFAULT NULL,
              tax_rate VARCHAR(20) DEFAULT NULL,
              tag VARCHAR(200) DEFAULT NULL,
              sites_name VARCHAR(20) DEFAULT NULL,
              crawling_time VARCHAR(20) DEFAULT NULL
              )ENGINE=INNODB DEFAULT CHARSET=utf8
			"""

        tx.execute(sql)
        tx.execute(
            "insert into ikjtao"+ today +" (goods_id,goods_name,goods_url,goods_picture_url,sale_price,market_price,"
                                         "sales_volume,comment_num,sup_category,sup_category_url,"
                                         "month_sales,brand,location,composition,application,item_no,commodity_brand,"
                                         "weight,tax_rate,tag,sites_name,crawling_time"
                                         " )\
             values (%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s)",
            (item['productId'],item['productName'],item['productUrl'],item['productImageUrl'],item['productSalePrice'],item['productMarketPrice'],
             item['salesVolume'],item['commentNum'],item['supCategory'],item['supCategoryUrl'],item['monthlySales'],item['brand'],
             item['location'],item['composition'],item['application'],item['itemNo'],item['commodityBrand'],
             item['weight'],item['taxRate'],item['tag'],"跨境淘".decode('utf-8'),datetime.datetime.now())
        )
        logger.info("Item stored in db: %s" ,item)

    def handle_error(self,e):
        # log.err(e)
        logger.info(e)

class IkjtaoPipeline(object):

    def __init__(self):
        today = datetime.date.today().strftime("%Y%m%d")
        str = '/home/ideas/CrawlData/'+today + '_kjtao_info.json'
        self.file = codecs.open(str,'w',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode('unicode_escape'))
        return item
