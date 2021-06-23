from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import undetected_chromedriver as uc

from MySpider import settings


class Login(object):
    def __init__(self, user, password, retry):
        uc.TARGET_VERSION = 91
        self.browser = uc.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.url = 'https://www.zhihu.com/signin'
        self.user = user
        self.password = password
        self.retry = retry  # 重试次数

    def onload_save_img(self, url):
        try:
            response = requests.get(url)
            save_as_path = '{0}{1}/{2}'.format(settings.STATIC_FILE, 'zhihu_captcha_test', response.url.split('/')[-1])
        except Exception as e:
            print('图片下载失败')
            raise e
        else:
            with open(save_as_path, 'wb') as f:
                f.write(response.content)

    def login(self):
        self.browser.get(self.url)
        login_element = self.browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[1]/div[2]')
        self.browser.execute_script("arguments[0].click();", login_element)
        time.sleep(1)

        # 输入账号
        username = self.wait.until(
            Ec.element_to_be_clickable((By.CSS_SELECTOR, '.SignFlow-account input'))
        )
        username.send_keys(self.user)
        # 输入密码
        password = self.wait.until(
            Ec.element_to_be_clickable((By.CSS_SELECTOR, '.SignFlow-password input'))
        )
        password.send_keys(self.password)

        # 登录框
        submit = self.wait.until(
            Ec.element_to_be_clickable((By.CSS_SELECTOR, '.Button.SignFlow-submitButton'))
        )
        submit.click()
        time.sleep(2)

        k = 1
        # while True:
        while k < self.retry:
            bg_img = self.wait.until(Ec.presence_of_element_located((By.CSS_SELECTOR, '.yidun_bgimg .yidun_bg-img')))
            background_url = bg_img.get_attribute('src')
            self.onload_save_img(background_url)

            refresh = self.browser.find_element_by_xpath('//*[@class="yidun_refresh"]')
            refresh.click()
            time.sleep(2)
            k += 1

        return None


if __name__ == '__main__':
    l = Login("15799655431", "zxcvbnm", 3)
    baidu_bce = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/zhihu_captcha'
    l.login()
