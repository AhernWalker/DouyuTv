# -*- coding: utf-8 -*-
import json
import scrapy
from Douyu.items import DouyuItem
from scrapy_redis.spiders import RedisSpider


class DouyuSpider(RedisSpider):
    """斗鱼直播间信息抓取"""
    name = 'douyu'
    # allowed_domains = ['douyutv.com', 'douyu.com']
    offset = 0
    base_url = 'http://api.douyutv.com/api/v1/live/{}/?limit=100&offset='
    # start_urls = ['https://www.douyu.com/directory']

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(DouyuSpider, self).__init__(*args, **kwargs)

    redis_key = 'douyuweb'

    def parse(self, response):
        """获取所有频道的简写, 并发送请求获取频道内所有房间的有效信息"""
        directory_list = response.xpath(
            '//*[@id="live-list-contentbox"]/li/a/@href').extract()

        for temp in directory_list:
            # 获取频道简称
            directory = temp.split('/')[-1]

            # 构建详细频道的url
            detail_url = self.base_url.format(directory)

            yield scrapy.Request(detail_url, callback=self.parse_item, meta={'detail_url': detail_url, 'directory': directory})

    def parse_item(self, response):
        """解析json数据"""
        directory = response.meta['directory']
        detail_url = response.meta['detail_url']

        # 将返回的文本转换为json格式的字典
        data_list = json.loads(response.body)['data']
        for data in data_list:
            item = DouyuItem()
            item['directory'] = directory
            item['nickname'] = data['nickname']
            item['online'] = data['online']
            item['uid'] = data['owner_uid']
            item['fans'] = data['fans']
            item['room_url'] = 'https://www.douyu.com/' + data['room_id']

            # print(item)
            yield item

        # 判断是否有翻页, 有的话再次调用parse_item函数
        if len(data_list) == 100:
            self.offset += 100
            next_url = detail_url + str(self.offset)
            yield scrapy.Request(next_url, callback=self.parse)
