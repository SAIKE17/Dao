# Encoding:UTF-8
# Project Name:Dao
# File:web_base.py
# Created on:2021年12月17日 09:49:33 by SAIKE, 1059436959@qq.com
#
import os
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Base:
    """
    1、获取网站cookie
    2、cookie不存在->登录获取cookie
    3、cookie存在->用cookie签到
    """

    def __init__(self, url):
        f = open("./website/login.json", 'r', encoding='UTF-8')
        self.login_info = json.loads(f.read())
        f.close()
        self.cookie_url = './website/cookies/'
        self.page_url = './website/pages/'
        # 添加自定义参数跳过cloud flare验证
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        caps = options.to_capabilities()
        self.browser = webdriver.Remote(command_executor='http://xxx.xxx.xxx.xxx:4444/wd/hub', desired_capabilities=caps)
        self.browser.get(url)
        # 将窗口最大化
        self.browser.maximize_window()

    def login_in(self, cookie_key, login_xpath):
        locator = (By.XPATH, login_xpath)
        # 让网页等待直到出现指定xpath，否则报错
        WebDriverWait(self.browser, 60, 0.3).until(expected_conditions.presence_of_element_located(locator))
        self.save_cookie(cookie_key)

    def get_cookie(self, cookie_key):
        cookie_file = self.cookie_url + cookie_key + '_cookies.json'
        if os.path.exists(cookie_file):
            file = open(cookie_file, 'r', encoding='UTF-8')
            cookie = json.loads(file.read())
            file.close()
            res = {
                "res": True,
                "msg": cookie,
            }
        else:
            res = {
                "res": False,
                "msg": 'Cookie文件不存在！',
            }
        return res

    def save_cookie(self, cookie_key):
        # 获取list的cookies
        dict_cookies = self.browser.get_cookies()
        # 转换成字符串保存
        json_cookies = json.dumps(dict_cookies)
        self.set_cookie(cookie_key, json_cookies)

    def set_cookie(self, cookie_key, json_cookies):
        with open(self.cookie_url + cookie_key + '_cookies.json', 'w', encoding='UTF-8') as f:
            f.write(json_cookies)
            f.close()

    def sign(self, cookie_key):
        list_cookies = self.get_cookie(cookie_key)

        # 往browser里添加cookies
        for cookie in list_cookies['msg']:
            cookie_dict = {
                'domain': cookie.get('domain'),
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.browser.add_cookie(cookie_dict)

        # 刷新网页,cookies才成功
        self.browser.refresh()

    def click(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    def get_page_source(self):
        # 打印网页源代码
        return self.browser.page_source

    def save_page(self, page_name, page):
        with open(self.page_url + page_name + '_page.html', 'w', encoding='UTF-8') as f:
            f.write(page)
            f.close()

    def __del__(self):
        # 运行结束,退出浏览器
        self.browser.quit()
