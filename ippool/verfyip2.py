import requests
from queue import Queue
from threading import Thread
from retrying import retry
from time import sleep
from lxml import etree
import redis,json

class TryIp(object):

    def __init__(self):
        self.url = "http://www.baidu.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
        self.url_queue = Queue()
        self.proxy_queue = Queue()
        self.new_proxy_queue = Queue()
        self.con = redis.StrictRedis(host='localhost',port=6379)
        self.con.delete('new_new_ip')

    def get_ip_from_redis(self):
        '''从数据库中获取ip'''
        lis = self.con.lrange('new_ip',0,-1)
        for each in lis:
            each = each.decode()
            each = eval(each)
            self.proxy_queue.put(each)

    def add_ip_from_newproxyqueue(self):
        '''将可用的代理存储到rdis中'''
        while True:
            ip = self.new_proxy_queue.get()
            if ip:
                self.con.lpush('new_new_ip',ip)
                self.new_proxy_queue.task_done()

    @retry(stop_max_attempt_number=3)
    def _parse_url(self,iproxy):
        response = requests.get(self.url, headers=self.headers,proxies=iproxy,timeout=5)
        assert response.status_code == 200
        html = etree.HTML(response.content)
        return html

    def parse_url(self):
        '''验证代理是否可用'''
        while True:
            proxy = self.proxy_queue.get()
            if proxy:
                con = 'http://'+proxy['ip']+':'+proxy['port']
                iproxy = {'http':con}
                try:
                    html = self._parse_url(iproxy)
                except Exception as e:
                    print(e, "*" * 10)
                    html = None
                if html:
                    print(iproxy)
                    self.new_proxy_queue.put(proxy)
                self.proxy_queue.task_done()

    def run(self):
        threading_list = []

        get_ip = Thread(target=self.get_ip_from_redis)
        threading_list.append(get_ip)
        #开启10个验证ip线程
        for i in range(10):
            print(i)
            t = Thread(target=self.parse_url)
            threading_list.append(t)

        set_ip = Thread(target=self.add_ip_from_newproxyqueue)
        threading_list.append(set_ip)

        for t in threading_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue, self.proxy_queue, self.new_proxy_queue]:
            q.join()

if __name__ == '__main__':
    tryip = TryIp()
    tryip.run()