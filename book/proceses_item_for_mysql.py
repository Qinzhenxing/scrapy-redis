#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import redis
import pymysql
import json


def process_item():
    # 创建redis数据库连接
    rediscli = redis.Redis(host="127.0.0.1", port=6379, db=0)

    # 创建mysql数据库连接 进行数据库的交互
    mysqlcli = pymysql.connect(host="127.0.0.1", user="root", password="mysql", database="python", port=3306, charset="utf8")
    offset = 0
    while True:
        # 将数据库从redis里pop出来

        source, data = rediscli.blpop("jd:items")
        print(data)
        print(type(data))
        item = json.loads(data.decode())
        item['book_authors'] = ','.join(item["book_authors"])
        if item["book_publish_date"] is '':
            item["book_publish_date"] = "None"

        print(item)
        # 创建mysql 操作游标对象执行mysql语句
        cursor = mysqlcli.cursor()

        cursor.execute("insert into jd(b_cate, x_title, x_href, book_img, bood_data_sku, book_name, book_authors,book_press,book_publish_date,book_href,book_price) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (item['b_cate'],item['x_title'],item['x_href'],item['book_img'],item['book_data_sku'],item['book_name'],item['book_authors'],item['book_press'],item['book_publish_date'],item['book_href'],item['book_price']))
        # 提交事务
        mysqlcli.commit()
        # 关闭游标
        cursor.close()
        offset += 1
        print(offset)





if __name__ == '__main__':
    # pymysql.install_as_MySQLdb()
    process_item()

