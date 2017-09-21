# -*- coding: utf-8 -*-
import json

import scrapy
from copy import deepcopy


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', "3.cn"]
    start_urls = ['http://book.jd.com/booksort']

    def parse(self, response):
        dt_list = response.xpath("//div[@id='booksort']/div[@class='mc']/dl/dt")
        for dt in dt_list:
            item={}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::*[1]/em")
            for em in em_list:
                item["x_title"] = em.xpath("./a/text()").extract_first()
                item["x_href"] = em.xpath("./a/@href").extract_first()
                item["x_href"] = "https:" + item["x_href"] if item["x_href"] is not None else None
                yield scrapy.Request(
                    item["x_href"],
                    callback= self.parse_book_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_book_list(self, response):
        item = deepcopy(response.meta["item"])
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_img"] = "https:" + item["book_img"] if item["book_img"] is not None else None
            item['book_data_sku'] = li.xpath("./div/@data-sku").extract_first()
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first()
            item["book_authors"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-name']/span[contains(@class,'author_type')]/a/text()").extract()
            item["book_press"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-store']/a/text()").extract_first()
            item["book_publish_date"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-date']/text()").extract_first()
            if item['book_data_sku'] is not None:
                item['book_href'] = li.xpath(".//div[@class='p-img']/a/@href").extract_first()
                item["book_href"] = "https:"+item["book_href"] if item["book_href"] is not None else None
                price_temp_url = "http://p.3.cn/prices/get?type=1&ext=11000000&pin=&pdtk=&pduid=1502078076997466357108&pdpin=&pdbp=0&skuid=J_{}"
                price_url = price_temp_url.format(item["book_data_sku"])

                yield scrapy.Request(
                    price_url,
                    callback=self.parse_book_price,
                    meta={"item": deepcopy(item)}
                )
        # 翻页
        next_url = response.xpath("//div[@class='page clearfix']/div[@class='p-wrap']/span[@class='p-num']/a[@class='pn-next']/@href").extract_first()

        if next_url is not None:
            next_url = "https:" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta=deepcopy(response.meta["item"])
            )

    def parse_book_price(self, response):
        item = deepcopy(response.meta["item"])
        # 拿到的是json数据转换成python类型数据（都是字符串类型）
        temp_price = json.loads(response.body.decode())
        item["book_price"] = temp_price[0]["op"]
        print("*"*100)
        yield item