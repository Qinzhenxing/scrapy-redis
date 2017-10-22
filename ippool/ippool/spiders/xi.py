# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ippool.items import IppoolItem


class XiSpider(CrawlSpider):
    name = 'xi'
    allowed_domains = ['66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="textlarge22"]/li[2]|//ul[@class="textlarge22"]/li[3]'), follow=True),
        Rule(LinkExtractor(allow=r'areaindex_1/\d+|areaindex_2/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        tr_list = response.xpath('//div[@id="footer"]//table/tr')
        tr_list = tr_list[2:] if tr_list else None
        if tr_list:
            for tr in tr_list:
                ip = tr.xpath('./td[1]/text()').extract_first()
                port = tr.xpath('./td[2]/text()').extract_first()
                if ip and port :
                    item = IppoolItem()
                    item['ip'] = ip
                    item['port'] = port
                    yield item
