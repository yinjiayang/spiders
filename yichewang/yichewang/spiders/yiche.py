# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yichewang.items import YichewangItem

class YicheSpider(CrawlSpider):
    name = 'yiche'
    allowed_domains = ['bitauto.com']
    start_urls = ['http://car.bitauto.com/xuanyi/koubei/']

    # 'http://car.bitauto.com/xuanyi/koubei/gengduo/1699-0-0-0-0-0-0-0-0-0-0--4-10.html'
    rules = (
        Rule(LinkExtractor(allow=r'1699-0-0-0-0-0-0-0-0-0-0--\d+-10.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        car_list = response.xpath('//div[@class="kb-list-box"]')
        item = YichewangItem()
        for pre in car_list:
            item['year'] = pre.xpath('./div[2]/div[1]/h6/text()').extract_first()
            item['price'] = pre.xpath('./div[2]/div[1]/div/span[1]/em/text()').extract_first()
            item['time'] = pre.xpath('./div[2]/div[1]/div/span[2]/text()').extract_first().strip()
            item['address'] = pre.xpath('./div[2]/div[1]/div/span[2]/text()').extract()[-1].strip()
            item['content'] = ''.join(pre.xpath('./div[2]/div/p/text()').extract()).strip()
            item['pub_time'] = pre.xpath('./div[2]/div/div[@class="mess-box"]/span[1]/text()').extract_first()
            item['youhao'] = pre.xpath('./div[2]/div/div[@class="mess-box"]/span[@class="yh"]/em/text()').extract_first()
            item['url'] = response.url
            # print(item)
            yield item