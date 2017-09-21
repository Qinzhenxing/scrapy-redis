from selenium import webdriver

import time
import json

class DouyuSpider:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver =webdriver.Chrome()

    def get_content_list(self):

        content_list = []
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        for li in li_list:
            item =  {}
            item["room_href"] = li.find_element_by_xpath("./a").get_attribute("href")
            item["room_title"] = li.find_element_by_xpath('./a').get_attribute("title")
            item["room_img"] = li.find_element_by_xpath('.//span[@class="imgbox"]/img').get_attribute("data-original")
            item["room_category"] = li.find_element_by_xpath(".//div[@class='mes-tit']//span[@class='tag ellipsis']").text
            item["room_anchor"] = li.find_element_by_xpath(".//div[@class='mes']/p/span[1]").text
            item["room_watch_num"] = li.find_element_by_xpath(".//div[@class='mes']/p/span[2]").text
            print(item)
            content_list.append(item)
        next_page = self.driver.find_elements_by_class_name("shark-page-next")
        next_page = next_page[0] if len(next_page) > 0 else None
        return content_list,next_page

    def save_content_list(self,  content_list):
        with open("douyu.txt", "a") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write("\n")
    def run(self):
        # url
        # 用自动测试浏览器 selenium
        self.driver.get(self.start_url)
        # 提取数据
        content_list, next_page = self.get_content_list()
        # 保存
        self.save_content_list(content_list)
        while next_page is not None:
            next_page.click()
            time.sleep(3)
            content_list,next_page = self.get_content_list()

            self.save_content_list(content_list)



    def __del__(self):
        self.driver.quit()

if __name__ == '__main__':
    douyu  = DouyuSpider()
    douyu.run()