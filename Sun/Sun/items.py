# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SunItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # 投诉编号
    url = scrapy.Field()  # 投诉详情url
    title = scrapy.Field()  # 投诉标题
    content = scrapy.Field()  # 投诉内容
    pass
