# -*- coding: utf-8 -*-
import scrapy
import re

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    # post 请求 寻找data参数构成一个字典
    def parse(self, response):
        formdata = {}
        formdata["utf8"] = response.xpath("//input[@name='utf8']/@value").extract_first()
        formdata["authenticity_token"] = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        formdata["commit"] = response.xpath("//input[@name='commit']/@value").extract_first()
        formdata["login"] = "noobpythoner"
        formdata["password"] = "zhoudawei123"

        # post 请求的方法 get请求的方法是Request
        yield scrapy.FormRequest(
            "https://github.com/session",
            formdata=formdata,
            callback=self.parse2
        )

    def parse2(self, response):
        print(re.findall(r"noobpythoner|NoobPythoner", response.body.decode(), re.S))

