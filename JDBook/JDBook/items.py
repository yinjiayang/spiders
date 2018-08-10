# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    """
    大分类，小分类，大分类页面url，小分类页面url
，封面图片链接，书名，详情页面url，作者，出版社，出版时间，价格

    """
    big_category = scrapy.Field()
    big_category_url = scrapy.Field()
    small_category = scrapy.Field()
    small_category_url = scrapy.Field()
    book_image_link = scrapy.Field()
    book_name = scrapy.Field()
    detail_url = scrapy.Field()
    author = scrapy.Field()
    pub_house = scrapy.Field()
    price = scrapy.Field()
    pub_time = scrapy.Field()


