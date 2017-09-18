# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'
# 使用了scrapy-redis 里的去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用了scrapy-redis里的去重组件 不使用scrapy的默认的去重
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 项目可以暂停 redis请求数据不丢失
SCHEDULER_PERSIST = True

# 选择其中一个
# 默认的scrapy-redis请求（按优先级顺序）队列形式
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 队列形式 请求先进先出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 栈形式 请求先进后出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
# 管道文件启动文件
ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    # 支持将数据存储到Redis数据库里，必须启动 （一般带有scrapy-redis都需要启动)
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
# 指定数据库的主机IP
REDIS_HOST = ""
# 指定数据库的端口号 默认的6379 不加引号
REDIS_PORT = 6379

# log 等级
# LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1
