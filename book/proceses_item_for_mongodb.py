#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import redis
import pymongo
import json

def process_item():
    # 创建数据库连接redis
    rediscli = redis.Redis(host="127.0.0.1", port=6379, db="0")

    # 创建MongoDB数据库连接
    mongocli = pymongo.MongoClient(host="127.0.0.1", port=27017)

    # 创建mongodb数据库名称表名称
    sheetname = mongocli["jd"]["jdchart"]
    offset = 0

    while True:
        # redis 数据表名 和 数据
        source, data = rediscli.blpop("jd:items")
        offset += 1
        # 将json对对象转换为python对象
        data = json.loads(data)
        # 讲数据表插入到sheetname表里
        sheetname.insert(data)
        print(offset)

if __name__ == '__main__':
    process_item()
