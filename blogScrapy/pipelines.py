#!/usr/bin/python2.7
#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem
from blogScrapy.items import CateItem,TagItem
from blogScrapy.spiders.shellCate_spider import ShellCateSpider

class BlogscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class CateSqlitePipeline(object):
    filename = "/var/www/blogScrapy/sql/main.db"
    
    def __init__(self):
        self.conn = sqlite3.connect(self.filename)

    def process_item(self, item, spider):
        if isinstance(item, CateItem):
            sql = 'insert into cate (cate) values ("%s")' % (item['cate'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('cate save finish')
        elif isinstance(item, TagItem):
            sql = 'insert into tag (tag) values ("%s")' % (item['tag'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('tag save finish')
        else:
            return item
