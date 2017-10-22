# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
logger = logging.getLogger(__name__)
import redis

class IppoolPipeline(object):
    def __init__(self):
        self.con = redis.StrictRedis(host='localhost',port=6379)


    def process_item(self, item, spider):
        logger.debug(item)
        self.con.lpush('ip',item)
        return item
