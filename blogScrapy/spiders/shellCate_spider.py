#!/usr/bin/python2.7
#coding=utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from blogScrapy.items import CateItem,TagItem
import re,sys

class ShellCateSpider(BaseSpider):
    """
    用于抓取shell网上的分类信息，并存储或到处为json文件
    """
    name = "shellcate"
    allowed_domains = ['shell909090.com']
    start_urls = [
        'http://shell909090.com/blog/',
        ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        items = []
        
        lis = hxs.select('//li')
        for li in lis:
            cl = li.select('@class').extract()

            if len(cl) > 0 and re.match(r'^cat-item\ cat-item-\d{2,3}$', cl[0]):
                cate = li.select('a/text()').extract()[0]
                item = CateItem()
                item['cate'] = cate
                items.append(item)
        
        return items

class ShellTagSpider(BaseSpider):
    """
    用于抓取shell网上的tag信息，并存储或导出为json文件
    """
    name = "shelltag"
    allowed_domains = ['shell909090.com']
    start_urls = [
        'http://shell909090.com/blog',
        ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        items = []
        
        tags = hxs.select('//div[@class="tagcloud"]/a/text()').extract()
        print tags
        items = []
        for tag in tags:
            item = TagItem()
            item['tag'] = tag
            items.append(item)
        
        return items

