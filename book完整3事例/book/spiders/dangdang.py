# -*- coding: utf-8 -*-
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
import scrapy


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    # 启动需要的键 再写一个start_url 当作值 在redis中启动 下面的键名称随便起
    redis_key = 'dangdang_start_url'
    # 动态域名
    allowed_domains = ['dangdang.com']



    def parse(self, response):
        div_list = response.xpath("//div[contains(@name, 'm403752_pid')]")
        print(div_list)
        for div in div_list[1:]: # 大分类分组
            item = {}
            item["b_cate"] = div.xpath(".//dl[@class='primary_dl']/dt/text()").extract_first()
            dl_list = div.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:  # 中间的分类分组
                item["m_cate"] = dl.xpath("./dt/a/@title").extract_first()
                a_list = dl.xpath("./dd/a")
                for a in a_list:  # 小分类分组
                    item["s_href"] = a.xpath("./@href").extract_first()
                    item["s_cate"] = a.xpath("./@title").extract_first()
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = deepcopy(response.meta['item'])
        li_list = response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item["book_name"] = li.xpath("./a/@title").extract_first()
            item["book_href"] = li.xpath("./a/@href").extract_first()
            item["book_desc"] = li.xpath("./p[@class='detail']/text()").extract_first()
            item["book_price"] = li.xpath("./p[@class='price']/span[@class='search_now_price']/text()").extract_first()
            item["book_origin_price"] = li.xpath(
                "./p[@class='price']/span[@class='search_pre_price']/text()").extract_first()
            item["book_comment_num"] = li.xpath(".//a[@class='search_comment_num']/text()").extract_first()
            item["book_author"] = li.xpath(".//a[@name='itemlist-author']/text()").extract()
            item["book_press"] = li.xpath(".//a[@name='P_cbs']/@title").extract_first()
            item["book_publish_date"] = li.xpath(
                ".//a[@name='itemlist-author']/../following-sibling::*[1]/text()").extract_first()
            item["come_from"] = "dangdang"
            yield item
        # 翻页
        next_url_temp = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url_temp is not None:
            yield scrapy.Request(
                "http://category.dangdang.com" + next_url_temp,
                callback=self.parse_book_list,
                # 要用最原始的item 需要写response.meta["item"]
                meta={"item": deepcopy(response.meta["item"])}

            )

