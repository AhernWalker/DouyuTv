# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.utils.project import get_project_settings
import scrapy


class DouyuPipeline(object):
    def __init__(self):
        self.file = open('douyu.json', 'w')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
        return item

    def close_spider(self, spider):
        self.file.close()
