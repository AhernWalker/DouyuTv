# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # 频道名
    directory = scrapy.Field()
    # 昵称
    nickname = scrapy.Field()
    # 房间链接
    room_url = scrapy.Field()
    # 唯一id
    uid = scrapy.Field()
    # 粉丝
    fans = scrapy.Field()
    # 在线人数
    online = scrapy.Field()

    
