#!/usr/bin/python2.7
#coding=utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from blogScrapy.items import CateItem,TagItem,BlogItem
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

class ShellBlogSpider(BaseSpider):
    """
    用于抓取blog内容，根据sitemap内容来找到博客链接
    """
    name = "shellblog"
    allowed_domains = ['shell909090.com']
    start_urls = [
        'http://shell909090.com/blog/sitemap.xml'
        ]
    
    def parse(self, response):
         hxs = HtmlXPathSelector(response)
         urls = hxs.select('//url/loc/text()').extract()
        
         items = []
        
         # url = urls[0]
         # items.append(self.make_requests_from_url(url).replace(callback=self.parse_blog))
         for url in urls:
             items.append(self.make_requests_from_url(url).replace(callback=self.parse_blog))
         return items
    
    def parse_blog(self, response):
        hxs = HtmlXPathSelector(response)
        
        items = []

        title = hxs.select('//h1[@class="entry-title"]/text()').extract() or ['']
        time = hxs.select('//time[@class="entry-date"]/text()').extract() or ['']
        blog = hxs.select('//div[@class="entry-content"]').extract() or ['']
        author = hxs.select('//footer/a[1]/text()').extract() or ['']
        cate = hxs.select('//footer/a[2]/text()').extract() or ['']
        tag = hxs.select('//footer/a[3]/text()').extract() or ['']
        comments = hxs.select('//ol[@class="commentlist"]/li').extract() or ['']

        item = BlogItem()
        item['title'] = title[0]
        item['pub_date'] = time[0]
        item['blog'] = blog[0]
        item['cate'] = cate[0]
        item['comments'] = comments
        item['tag'] = tag
        item['author'] = author
        items.append(item)
        print '======================'
        return items

