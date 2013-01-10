# Scrapy settings for blogScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'blogScrapy'

SPIDER_MODULES = ['blogScrapy.spiders']
NEWSPIDER_MODULE = 'blogScrapy.spiders'

ITEM_PIPELINES = ['blogScrapy.pipelines.CateSqlitePipeline',]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'blogScrapy (+http://www.yourdomain.com)'
