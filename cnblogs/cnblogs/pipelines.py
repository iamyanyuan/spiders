# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class CnblogsPipeline(object):
    def process_item(self, item, spider):
        return item


class BlogsCsvPipeline(object):
    """保存数据到csv文件中"""

    # def __init__(self):
    #     with open('blogs.csv', 'a', encoding='utf_8_sig', newline='') as f:
    #         fielname = ['title', 'release_t',  'tags',
    #                 'come_from', 'url', 'comment_count', 'read_count', 'diggnum',
    #                 'url_obj_id']
    #         self.writer = csv.DictWriter(f, fieldnames=fielname)
    #         self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == 'cnblog':
            # print(item)
            with open('blogs.csv', 'a', encoding='utf_8_sig', newline='') as f:
                w = csv.DictWriter(f, item.keys())
                w.writerow(item)

            return item
