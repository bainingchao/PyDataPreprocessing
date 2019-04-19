# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonItemExporter
import codecs

class BolespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 调用scrapy提供的json export导出json文件
class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 将爬取的数据字段存储在mysql数据

import MySQLdb
import MySQLdb.cursors

# MYSQL数据库存储方法1
class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'test', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into myarticles(title, createdate,url,dianzan,soucang,comment) VALUES(%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["dianzan"],item["soucang"],item["comment"]))
        self.conn.commit()
