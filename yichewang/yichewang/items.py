# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YichewangItem(scrapy.Item):
    # define the fields for your item here like:
    year = scrapy.Field()
    price = scrapy.Field()
    time = scrapy.Field()
    address = scrapy.Field()
    content = scrapy.Field()
    youhao = scrapy.Field()
    pub_time = scrapy.Field()
    url = scrapy.Field()



    pass
