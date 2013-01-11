from scrapy.contrib.spiders import XMLFeedSpider
from blogScrapy.items import BlogscrapyItem

class FeedtestSpider(XMLFeedSpider):
    name = 'feedTest'
    allowed_domains = ['shell909090.com']
    start_urls = ['http://www.shell909090.com/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = BlogscrapyItem()
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i
