# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose

class BolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 设置提取字段的实体类
class JobBoleItem(scrapy.Item):
    title = scrapy.Field() # 文章题目
    create_date = scrapy.Field() #发布时间
    url =  scrapy.Field() #当前文章url路径
    dianzan = scrapy.Field() #点赞数
    soucang = scrapy.Field() # 收藏数
    comment = scrapy.Field() # 评论数