# -*- coding: utf-8 -*-
import re

import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['https://renren.com/327550029/profile']

    # 重新定义一个start_requests(self):
    # 因为腰带cookie
    def start_requests(self):
        cookies = "anonymid=j3jxk555-nrn0wh; _r01_=1; _ga=GA1.2.1274811859.1497951251; depovince=BJ; jebecookies=3b5ddf36-7fbf-413d-961f-2a0048673000|||||; JSESSIONID=abc2vMurtusBV-CwkE65v; ick_login=1cf5cda7-8502-46f4-869f-23e693f3dba3; _de=BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5; p=1dd97dfb673615b652e3b4101ff480859; first_login_flag=1; ln_uact=mr_mao_hacker@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20140529/1055/h_main_9A3Z_e0c300019f6a195a.jpg; t=efc0d2f21fc02656938071d968659e389; societyguester=efc0d2f21fc02656938071d968659e389; id=327550029; xnsid=8587309c; loginfrom=syshome; ch_id=10016; wp_fold=0"
        # 1cookies 参数是字典
        cookies = {i.split("=")[0]:i.split("=")[-1] for i in cookies.split(";")}
        start_url = self.start_urls[0]
        yield scrapy.Request(
            start_url,
            callable = self.parse,
            cookies = cookies
        )



    def parse(self, response):
        print(re.findall(r"毛兆军", response.body.decode(), re.S))
        yield scrapy.Request(
            "http://www.renren.com/327550029/profile?v=info_timeline",
            callback = self.parse2
        )
    def parse2(self, response):

        print("*"*10)
        print(re.findall(r"毛兆军", response.body.decode(), re.S))