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
import sys,traceback,time


class BlogscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class ShellSavePipeline(object):
    # filename = "/var/www/blogScrapy/sql/main.db"
    filename = "/var/www/blog/sql/main.db"
    
    def __init__(self):
        self.conn = sqlite3.connect(self.filename)

    def process_item(self, item, spider):
        if isinstance(item, CateItem):
            sql = 'insert into webblog_category (name,create_time, desc, category_pv) values ("%s", "2012-12-23 03:07:42.663000", "", 0)' % (item['cate'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('cate save finish')
        
        elif isinstance(item, TagItem):
            sql = 'insert into webblog_tag (tag_name, desc, create_time, tag_pv) values ("%s", "unknow", "2012-12-23 03:07:42.663000", 0 )' % (item['tag'],)
            self.conn.execute(sql)
            self.conn.commit()
            raise DropItem('tag save finish')
        
        # blog save,include comment, category and tags
        elif isinstance(item, BlogItem):
            try:
                catesql = "select category_id from webblog_category where name like ?" 
                cate = self.conn.execute(catesql, ('%'+item['cate']+'%',)).fetchall()
                if len(cate) >= 1:
                    cate_id = cate[0][0]
                else:
                    cate_id = 1 # 随机处理
            
                blogsql = "insert into blog (category_id, title, content, pub_time, blog_pv, is_closed) values (?,?,?,?,?,?)"
                blog = self.conn.execute(blogsql,(cate_id, item['title'], item['blog'], time.strftime('%Y-%m-%d'), 0, 0))
                self.conn.commit()
                blog_id = blog.lastrowid
                if len(item['comments']) > 0:
                    for comment in item['comments']:
                        commentsql = "insert into webblog_comment (author_name, author_email, content, is_close, blog_id, comment_up) values (?, ?, ?, ?, ?, ?)"
                        self.conn.execute(commentsql, ('shell', 'shell909090@gmail.com', comment, 0, blog_id, 0))
                        self.conn.commit()
                tagsql1 = "select tag_id from webblog_tag where tag_name like ?"
                if len(item['tag']) >= 1:
                    tag = item['tag'][0]
                    tag = self.conn.execute(tagsql1, ('%'+tag+'%',)).fetchall()
                    if len(tag) >= 1:
                        tag_id = tag[0][0]
                    else:
                        tag_id = 1 # 随机处理
                        tagsql2 = "insert into webblog_tag_blog (tag_id, blog_id) values (?, ?)"
                        self.conn.execute(tagsql2, (tag_id, blog_id))
                        self.conn.commit()
                raise DropItem('blog save finish')
            except:
                traceback.print_exc()
                print "---------------------------------------"
                print "blog %s crawl fail" % item['title']
                return item
        return item
