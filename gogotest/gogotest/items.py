# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GogotestItem(scrapy.Item):
    
    nane = scrapy.Field()
    url = scrapy.Field()
    refurl = scrapy.Field()
    title = scrapy.Field()
    

class BlogPost(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
