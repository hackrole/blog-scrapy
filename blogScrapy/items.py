#!/usr/bin/python2.7
#coding=utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BlogscrapyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class BaseItem(Item):
    """
    只保留博客url地址和网页内容
    """
    url = Field()
    html_content = Field()

class JsonItem(Item):
    """
    到处为json格式文件的item
    """
    title = Field()
    pub_date = Field()
    author = Field()
    blog_content = Field()
    cate = Field() # 分类
    tags = Field() # tags
    comments = Field # 评论列表
    
class TagItem(Item):
    """
    用于抓取tag列表的item
    """
    tag = Field()
    
class CateItem(Item):
    """
    用于抓取分类列表的item
    """
    cate = Field()
    
    
