# -*- coding: utf-8 -*-

import scrapy
from urllib import parse
import re
import requests
import json
from blogs_spider.items import BlogsSpiderItem
from blogs_spider.utils.common import get_md5


class BlogsSpider(scrapy.Spider):
    name = 'blogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']

    def parse(self, response):
        """
        1.获取新闻列表页中的url并交给scrapy进行下载后的调用和相应的解析
        2.获取下一页的URL并交给scrapy进行下载，下载完成后交给parse继续跟进
        """
        # nodes = response.xpath('//div[@class="content"]')[:3]
        nodes = response.xpath('//div[@class="content"]')

        for li in nodes:
            art_url = li.xpath('./h2/a/@href').extract_first()  # 文章url
            img_url = li.xpath('./div[@class="entry_summary"]/a/img/@src').extract_first() if len(
                li.xpath('./div[@class="entry_summary"]/a/img/@src')) > 0 else None

            yield scrapy.Request(url=parse.urljoin(response.url, art_url), callback=self.parse_detail,
                                 meta={'img_url': img_url})

        # 翻页
        # next_url = response.xpath('//a[contains(text(), "Next")]/@href').extract_first()
        # next_url = parse.urljoin(response.url, next_url)
        # print('url:', next_url)
        # yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        """抓取详情信息"""
        item = BlogsSpiderItem()

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
            item['img_url'] = [response.meta.get('img_url', [])]
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
        yield item
