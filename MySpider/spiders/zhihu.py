import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def start_requests(self):
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # chrome_option.binary_location = 'G:/MySpider/MySpider/chromedriver.exe'
        browser = webdriver.Chrome(executable_path='G:/MySpider/MySpider/chromedriver.exe', chrome_options=chrome_option)
        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_css_selector('.SignFlow-tabs div:nth-child(2)').click()
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').clear()
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('15797760661')
        browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').clear()
        browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys('wangkai1995')
        browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
        time.sleep(10)

    def parse(self, response):
        pass
