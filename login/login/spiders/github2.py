# -*- coding: utf-8 -*-
import re

import scrapy


class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']
    # post请求 如果表单的action有连接地址 就可以直接利用表单的input输入帐号密码
    # 不需要找data和携带cookie
    def parse(self, response):
        formdata = {
            "login": "noobpythoner",
            "password": "zhoudawei123"

        }
        yield scrapy.FormRequest.from_response(
            #
            # 发送的响应不是连接

            response,
            formdata = formdata,
            callback = self.parse2
        )
    def parse2(self, response):
        print(re.findall(r"noobpythoner|NoobPythoner", response.body.decode(), re.S))