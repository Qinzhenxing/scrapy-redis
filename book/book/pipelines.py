# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import time

# 存mongodb 需要倒入的  最重要的需要在
# from pymongo import MongoClient
# from book.book.settings import MONGO_PORT, MONGO_HOST


class BookPipeline(object):
    # 连接mongodb数据库
    # def open_spider(self, spider):
    #     client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    #     # 创建mongodb的集合 （没有，自动创建）
    #     self.collection = client["book"]["jd"]




    def process_item(self, item, spider):
        item["book_name"] = self.handle_item(item["book_name"])
        item["book_authors"] = self.handle_item(item["book_authors"])
        item["book_publish_date"] = self.handle_item(item["book_publish_date"])
        print(item)
        time.sleep(3)
        # 保存mongodb数据库添加 字典形式
        # self.collection.insert(item)
        return item


    def handle_item(self, content):
        # 判断是不是
        if isinstance(content, list):
            return [i.strip() for i in content]
        if isinstance(content, str):
            content = re.sub(r"\s+", "", content)
            return content