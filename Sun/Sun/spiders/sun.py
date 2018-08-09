# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Sun.items import SunItem


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4']

    # 提取翻页的链接
    # http://wz.sun0769.com/index.php/question/questionType?type=4&page=30
    # 提取详情的url
    # http://wz.sun0769.com/html/question/201808/381599.shtml
    rules = (
        # 翻页
        Rule(LinkExtractor(allow=r'http://wz.sun0769.com/index.php/question/questionType\?type=4&page=\d+'), callback='parse_item', follow=True),
        # 详情url
        Rule(LinkExtractor(allow=r'http://wz.sun0769.com/html/question/\d+/\d+.shtml'), callback='parse_detail_content', follow=True),
    )

    # node_list = response.xpath('//*[@id="morelist"]/div/table[2]/tr/td/table/tr')

    def parse_item(self, response):
        # 实例化Item
        item = SunItem()
        item['id'] = response.xpath('//*[@id="morelist"]/div/table[2]/tr/td/table/tr/td[1]/text()').extract_first()
        item['title'] = response.xpath('//*[@id="morelist"]/div/table[2]/tr/td/table/tr/td[2]/a[2]/text()').extract_first()

        return item

    def parse_detail_content(self, response):
        item = SunItem()
        item['url'] = response.url
        item['content'] = ''.join([i.strip() for i in response.xpath('/html/body/div[6]/div/div[2]/div[1]/div[2]/text()|/html/body/div[6]/div/div[2]/div[1]/text()').extract()])

        return item