# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class MyspidersPipeline(object):

    def __init__(self):
        self.file = open('tencent.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        str_data = self.file.write(json.dumps(dict(item), ensure_ascii=False))
        return item

    def __del__(self):
        self.file.close()