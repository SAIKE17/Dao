# Encoding:UTF-8
# Project Name:Dao
# File:smzdm.py
# Created on:2021年12月21日 11:39:33 by SAIKE, 1059436959@qq.com
#
import time
import traceback

from .web_base import Base


class Smzdm(Base):
    web_key = 'smzdm'
    web_url = 'https://www.smzdm.com/'

    def __init__(self):
        Base.__init__(self, self.web_url)
        name_temp = self.login_info.get(self.web_key + '_username')
        pswd_temp = self.login_info.get(self.web_key + '_password')
        self.username = name_temp if name_temp is not None else ''
        self.password = pswd_temp if pswd_temp is not None else ''

    def sign(self):
        try:
            res = True
            msg = '[' + self.web_key.upper() + '] 签到成功'
            # 读取cooke
            cookie = Base.get_cookie(self, self.web_key)

            # cookie不存在则进行登录
            if 0 == cookie['res']:
                # 点击登录按钮
                self.browser.find_element_by_xpath("//a[@class='J_login_trigger']").click()
                time.sleep(1)
                # 跳转到iframe
                self.browser.switch_to.frame('J_login_iframe')
                # 点击用账号密码登录
                self.browser.find_element_by_xpath("//div[@class='qrcode-change J_qrcode_change']").click()
                time.sleep(1)
                # 输入账号密码
                self.browser.find_element_by_id('username').send_keys(self.username)
                self.browser.find_element_by_id('password').send_keys(self.password)
                # 跳转回默认html
                self.browser.switch_to.default_content()
                Base.login_in(self, self.web_key, "//a[@class='name-link']")

            # 登录
            Base.sign(self, self.web_key)
            time.sleep(3)

            Base.click(self, "//a[@class='J_punch']")
            time.sleep(1)
            # Base.click(self, "//a[@class='J_punch']")

            # 签到成功保存cookie
            Base.save_cookie(self, self.web_key)

            # 获取信息
            days = self.browser.find_element_by_xpath("//a[@class='J_punch']").text
            msg += "\n" + days
        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
