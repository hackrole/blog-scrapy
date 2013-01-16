#!/usr/bin/python2.7
#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem
from blogScrapy.items import CateItem,TagItem,BlogItem
from blogScrapy.spiders.shellCate_spider import ShellCateSpider
# import sys

# sys.path.insert(0, '/var/www/blog')
# from blog import settings
# DJANGO_SETTINGS_MODULE = settings

# from webblog.models import Blog,Category


class BlogscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class CateSqlitePipeline(object):
    # filename = "/var/www/blogScrapy/sql/main.db"
    filename = "/var/www/blog/sql/main.db"
    
    def __init__(self):
        self.conn = sqlite3.connect(self.filename)

    def process_item(self, item, spider):
        if isinstance(item, CateItem):
            sql = 'insert into webblog_category (name,create_time,category_rate) values ("%s", "2012-12-23 03:07:42.663000", 0)' % (item['cate'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('cate save finish')
        elif isinstance(item, TagItem):
            sql = 'insert into webblog_tag (tag_name, desc, create_time, tag_rate) values ("%s", "unknow", "2012-12-23 03:07:42.663000", 0 )' % (item['tag'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('tag save finish')
        elif isinstance(item, BlogItem):
            sql1 = "select category_id from webblog_category where name like '%%%s%%'" % (item['cate'],)
            cate = self.conn.execute(sql1).fetchall()[0][0]
            # cate = Category.objects.filter(name__like=item['cate'])[0]
            # print type(item['blog'])
            sql = 'insert into blog (category_id_id, title, desc, content, pub_time, update_time, is_pub, is_close, is_visiable) values (%s, "%s", "unknow", \'%s\', "2012-12-23 03:07:42.663000", "2012-12-23 03:07:42.663000", 0, 0, 0)' % (cate, item['title'], item['blog'])
            print sql
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('tag save finish')
        return item
