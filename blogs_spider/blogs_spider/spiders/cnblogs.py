# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from urllib import parse
from blogs_spider.utils.common import get_md5


class CnblogsSpider(CrawlSpider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://news.cnblogs.com']

    rules = (
        Rule(LinkExtractor(allow=r'/n/\d+'), callback='parse_item'),  # 获取详情页url

    )

    def parse_item(self, response):
        item = {}
        n_id = re.match('.*?(\d+)', response.url)
        if n_id:
            item["title"] = response.css('#news_title a::text').extract_first()
            t = response.css('span.time::text').extract_first()
            item["release_t"] = re.search('(\d+.*)', t).group(1)
            tag_list = response.css('.news_tags a::text').extract()
            item["tags"] = ','.join(tag_list)
            item["come_from"] = response.css('#come_from a::text').extract_first() if len(
                response.css('#come_from a::text')) > 0 else None
            # item["news_content"] = response.css('#news_body').extract()[0]  # 文章内容
            news_id = n_id.group(1)
            json_url = 'https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId={}'.format(news_id)
            item['url'] = response.url

            yield scrapy.Request(url=json_url, meta={'item': item}, callback=self.parse_json)

    def parse_json(self, response):
        """解析json数据"""
        item = response.meta['item']
        html_json = requests.get(response.url)
        data = html_json.json()
        item["comment_count"] = data['CommentCount']  # 评论数
        item["read_count"] = data['TotalView']  # 阅读量
        item["diggnum"] = data['DiggCount']  # 点赞数
        item['url_obj_id'] = get_md5(item['url'])
        print(item)
        yield item

