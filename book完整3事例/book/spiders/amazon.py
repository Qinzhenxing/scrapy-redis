# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 创建crawlspider命令 scrapy genspider -t crawl amazon  amazon.cn (爬虫名称，域名)
# 进来修改继承父类 因为是分布式
from scrapy_redis.spiders import RedisCrawlSpider

class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    redis_key = "amazon_start_url"

    rules = (
        # 提取分类url的规则
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='categoryRefinementsSection']/ul/li")), follow=True),
        # 提取图书详情页的规则
        Rule(LinkExtractor(restrict_xpaths=("//*[@class='s-item-container']//h2/..",)), callback="parse_book_detail"),
        # 获取分类下一页的规则
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)), follow=True),
    )

    def parse_book_detail(self, response):
        item = {}
        item["book_title"] = response.xpath("//title/text()").extract_first()
        item["book_info"] = response.xpath(
            "//div[@id='detail_bullets_id']//div[@class='content']/ul/li//text()").extract()
        item["book_cate_list"] = response.xpath(
            "//ul[@class='zg_hrsr']/li[1]/span[@class='zg_hrsr_ladder']//a/text()").extract()
        item["book_author"] = response.xpath("//div[@id='byline']//text()").extract()
        item["is_ebook"] = "Kindle电子书" in item["book_title"]
        if item["is_ebook"]:
            item["book_price"] = response.xpath("//tr[@class='kindle-price']/td[2]/text()").extract_first()
            # item["ebook_img"] = response.xpath("//div[@id='ebooks-img-canvas']/img/@src").extract_first()
        else:
            item["book_price"] = response.xpath("//div[@id='buyNewSection']//text()").extract()
            # item["book_img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
        # 通过管道的时候可以进行数据的处理来分辨 那个处理那个那个应该储存到那里
        item["come_from"] = "amazon"
        yield item
