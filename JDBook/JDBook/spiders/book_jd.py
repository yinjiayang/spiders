# -*- coding: utf-8 -*-
import scrapy
from JDBook.items import JdbookItem
import json
from scrapy_redis.spiders import RedisSpider


class BookJdSpider(RedisSpider):
    name = 'book_jd'
    # allowed_domains = ['book.jd.com', 'list.jd.com', 'p.3.cn']
    # start_urls = ['https://book.jd.com/booksort.html']
    redis_key = 'book:start_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(BookJdSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        # 获取大分类列表
        big_category_list = response.xpath('//*[@id="booksort"]/div[@class="mc"]/dl/dt')
        # print(big_category_list)
        for big_cate in big_category_list:
            """
            preceding-sibling 选取当前节点之前的所有同级节点 
            following-sibling 选取当前节点之后的所有同级节点
            """

            big_category_url = 'https:' + big_cate.xpath('./a/@href').extract_first()
            big_category = big_cate.xpath('./a/text()').extract_first()
            small_category_list = big_cate.xpath('./following-sibling::*[1]')
            # small_category_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dd[1]')
            for small_cate in small_category_list:
                small_category_url = 'https:' + small_cate.xpath('./em/a/@href').extract_first()
                small_category = small_cate.xpath('./em/a/text()').extract_first()

                data = {
                    'big_category_url': big_category_url,
                    'big_category': big_category,
                    'small_category_url': small_category_url,
                    'small_category': small_category


                }
                yield scrapy.Request(
                    url=small_category_url,
                    callback=self.parse_small_category,
                    meta={'meta_1': data})

    def parse_small_category(self, response):
        """爬取书的详情"""
        data = response.meta['meta_1']
        print(data)
        all_book_detail_list = response.xpath('//*[@id="plist"]/ul/li')
        for book in all_book_detail_list:
            item = JdbookItem()  # 实例化
            item['big_category_url'] = data['big_category_url']
            item['big_category'] = data['big_category']
            item['small_category_url'] = data['small_category_url']
            item['small_category'] = data['small_category']
            # '//*[@id="plist"]/ul/li/div/div[@class="p-img"]/a/img/@src'
            item['book_image_link'] = book.xpath('./div/div[@class="p-img"]/a/img/@src').extract_first()
            # '//*[@id="plist"]/ul/li/div/div[@class="p-name"]/a/em/text()'
            # '//*[@id="plist"]/ul/li/div/div/div[2]/div[1]/div[@class="p-name"]/a/em/text()'
            item['book_name'] = book.xpath(
                './div/div[@class="p-name"]/a/em/text()|./div/div[2]/div[1]/div[@class="p-name"]/a/em/text()|//*[@id="hotsale"]/div[2]/div/dl[2]/dd/div[1]/a/text()'
            ).extract_first().strip()
            # '//*[@id="plist"]/ul/li/div/div[@class="p-name"]/a/@href'
            item['detail_url'] = 'https:' + book.xpath(
                './div/div[@class="p-name"]/a/@href|//*[@id="hotsale"]/div[2]/div/dl[2]/dt/a/@href'
            ).extract_first()
            # '//*[@id="plist"]/ul/li/div/div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span/a/text()'
            item['author'] = book.xpath(
                './div/div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span/a/text()').extract_first()
            # '//*[@id="plist"]/ul/li/div/div[@class="p-bookdetails"]/span[@class="p-bi-store"]/a/text()'
            item['pub_house'] = book.xpath(
                './div/div[@class="p-bookdetails"]/span[@class="p-bi-store"]/a/text()').extract_first()
            # '//*[@id="plist"]/ul/li/div/div[@class="p-bookdetails"]/span[@class="p-bi-date"]/text()'
            item['pub_time'] = book.xpath(
                './div/div[@class="p-bookdetails"]/span[@class="p-bi-date"]/text()').extract_first()
            # 获取商品价格的url
            # '//*[@id="plist"]/ul/li[1]/div/@data-sku'
            data_sku = book.xpath('./div/div[9]/a[1]/@data-sku').extract_first()
            # print(data_sku)
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}%2C&pduid=15333024534481747413727'.format(data_sku)

            yield scrapy.Request(url=price_url, callback=self.parse_price, meta={'meta_2': item})
        # 翻页
        next_page = response.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract_first()
        if next_page is not None:
            next_url = 'https://list.jd.com' + next_page
            yield scrapy.Request(url=next_url, callback=self.parse_small_category)

    def parse_price(self, response):
        item = response.meta['meta_2']

        """[
{
"op": "81.00",
"m": "108.00",
"tpp": "79.00",
"id": "J_12090377",
"up": "tpp",
"p": "81.00"
}
]"""
        item['price'] = json.loads(response.body.decode())[0]['op']
        yield item