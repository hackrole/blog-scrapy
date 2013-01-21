#!/usr/bin/python2.7
#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem
from blogScrapy.items import CateItem,TagItem,BlogItem
from blogScrapy.helps import BlogSaveHelps
import sys,traceback,time


class BlogscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class BlogSavePipeline(object):
    """
    用于将blog的相关信息保存在sqlite表中
    """
    
    def __init__(self):
        self.help = BlogSaveHelps()

    def process_item(self, item, spider):
        if isinstance(item, CateItem):
            self.help.saveCate(item['cate'])
            raise DropItem('cate save finish')
        
        elif isinstance(item, TagItem):
            self.help.saveTag(item['tag'])
            raise DropItem('tag save finish')
        
        # blog save,include comment, category and tags
        elif isinstance(item, BlogItem):
            self.saveBlog(item)  
            raise DropItem('blog save finish')
        return item
