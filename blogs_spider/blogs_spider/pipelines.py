# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json
import pymysql
from scrapy.pipelines.images import ImagesPipeline


class BlogsSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlBlogsPipleline(object):
    """存储到MySQL"""

    def open_spider(self, spider):
        if spider.name == 'blogs':
            self.coon = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='mysql',
                                        database='python_db', charset='utf8')
            self.coursor = self.coon.cursor()

    def process_item(self, item, spider):
        if spider.name == 'blogs':
            item_list = []
            item_list.append(item.get('title', ''))
            item_list.append(item.get('url', ''))
            item_list.append(item.get('release_t', ''))
            item_list.append(item.get('tags', ''))
            item_list.append(item.get('come_from', ''))
            item_list.append(item.get('comment_count', 0))
            item_list.append(item.get('read_count', 0))
            item_list.append(item.get('diggnum', 0))
            item_list.append(item.get('url_obj_id', ''))
            my_sql = """
                insert into newblogs(title, url, release_t, tags, come_from, comment_count, read_count, diggnum, url_obj_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            self.coursor.execute(my_sql, tuple(item_list))  # 执行sql语句
            self.coon.commit()
            return item

    def close_spider(self, spider):
        """关闭数据库"""
        if spider.name == 'blogs':
            self.coursor.close()
            self.coon.close()


class JsonBlogsPipleline(object):
    """自定义json文件的导出"""

    def open_spider(self, spider):
        if spider.name == 'blogs':
            self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        if spider.name == 'blogs':
            lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file.write(lines)
            return item

    def close_spider(self, spider):
        if spider.name == 'blogs':
            self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    """自定义保存图片"""

    def item_completed(self, results, item, info):
        if 'img_url' in item:
            img_url = [item.get('img_url', '')]
            image_file_path = ''
            for ok, value in results:
                image_file_path = value['path']
            item['img_path'] = image_file_path
        return item