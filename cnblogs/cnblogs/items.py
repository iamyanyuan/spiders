# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    release_t = scrapy.Field()
    tags = scrapy.Field()
    come_from = scrapy.Field()
    comment_count = scrapy.Field()
    read_count = scrapy.Field()
    diggnum = scrapy.Field()
    url_obj_id = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()
    news_content = scrapy.Field()

