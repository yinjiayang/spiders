# -*- coding: utf-8 -*-
import scrapy
from myspiders.items import MyspidersItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        # 获取所有节点数据
        node_list = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')
        for node in node_list:
            item = MyspidersItem()
            item['profession'] = node.xpath('./td[1]/a/text()').extract()[0]
            item['link'] = 'https://hr.tencent.com/' + node.xpath('./td[1]/a/@href').extract()[0]
            # 提取补刀默认值为None，确定只有一条数据的时候使用
            item['category'] = node.xpath('./td[2]/text()').extract_first()
            item['num'] = node.xpath('./td[3]/text()').extract()[0]
            item['address'] = node.xpath('./td[4]/text()').extract()[0]
            item['pub_date'] = node.xpath('./td[5]/text()').extract()[0]

            yield scrapy.Request(url=item['link'], callback=self.parse_detail, meta={'key': item})

        # 翻页
        next_url = response.xpath('//*[@id="next"]/@href').extract_first()
        if next_url is not None:
            next_url = 'https://hr.tencent.com/' + next_url
            yield scrapy.Request(url=next_url, callback=self.parse)

    # 爬取工作职责和工作要求并一起返回给引擎
    def parse_detail(self, response):
        item = response.meta().get('key')
        item['job_duty'] = ''.join(response.xpath('//tr[3]/td/ul/li/text()').extract())
        item['job_requirmen'] = ''.join(response.xpath('//tr[4]/td/ul/li/text()').extract())
        yield item
