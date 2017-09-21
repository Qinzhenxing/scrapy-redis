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
        if item.get("come_from") == "dangdang":
            item = self.handle_dangdang_item(item)
            print(item)
        elif item.get("come_from") == "amazon":
            item = self.handle_amazon_item(item)
            print(item)
        else:
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

    def handle_dangdang_item(self, item):
        item["b_cate"] = re.sub(r"\s+", "", item["b_cate"])
        if item["book_publish_date"] is not None:
            item['book_publish_date'] = item['book_publish_date'].replace("/", "").strip()
        return item

    def handle_amazon_item(self, item):
        book_title_temp = re.findall(r"《(.*?)》", item["book_title"])
        if len(book_title_temp) > 0:
            item["book_title"] = book_title_temp[0]

        item["book_info"] = self.process_list(item["book_info"])
        temp_book_info = "_".join(item["book_info"])
        book_press = re.findall(r"出版社:_(.*?出版社)", temp_book_info)
        if len(book_press) < 1:
            book_press = None
        else:
            book_press = book_press[0]
        item["book_press"] = book_press
        item["book_publish_date"] = re.findall(r"\d+年\d+月\d+日", temp_book_info)
        item["book_publish_date"] = item["book_publish_date"][0] if len(item["book_publish_date"]) > 0 else None
        item["book_isbn"] = re.findall(r"ISBN:_(.*?)_", temp_book_info)
        item["book_isbn"] = item["book_isbn"][0].split(",")[0] if len(item["book_isbn"]) > 0 else None

        # for i in range(len(item["book_cate_list"])):
        #     item["cate_{}".format(i+1)] = item["book_cate_list"][i]
        item["book_author"] = self.process_list(item["book_author"])
        item["book_price"] = self.process_list(item["book_price"])
        item["book_price"] = re.findall(r"￥(.*?)_", "_".join(item["book_price"]))
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) > 0 else None
        item.pop("book_info")
        # item.remove("book_info")
        return item

    def process_list(self, temp_list):
        temp_list = [re.sub(r"\n|\s+", "", i) for i in temp_list]
        temp_list = [i for i in temp_list if len(i) > 1]
        return temp_list

