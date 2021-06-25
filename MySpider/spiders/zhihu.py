import time

import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from MySpider.utils.code_and_login import Login


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    custom_settings = {
        'COOKIES_ENABLED': True
    }

    def start_requests(self):
        # chrome_option = Options()
        # chrome_option.add_argument('--disable-extensions')
        # chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # browser = webdriver.Chrome(executable_path='G:/MySpider/MySpider/chromedriver.exe', chrome_options=chrome_option)
        # browser.get('https://www.zhihu.com/signin')
        # browser.find_element_by_css_selector('.SignFlow-tabs div:nth-child(2)').click()
        # browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').clear()
        # browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('15793326061')
        # browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').clear()
        # browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys('warrfff3w95')
        # browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
        # time.sleep(10)
        zhihu_login = Login("15797760661", "wangkai1995", 6)
        cookie_dict = zhihu_login.login(True)
        print(cookie_dict)
        for url in self.start_urls:
            yield Request(url, cookies=cookie_dict, dont_filter=True, callback=self.parse)

    def parse(self, response, **kwargs):
        pass
