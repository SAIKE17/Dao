# Encoding:UTF-8
# Project Name:Dao
# File:hifini.py
# Created on:2021年12月17日 09:45:16 by SAIKE, 1059436959@qq.com
#
import time
import traceback

from .web_base import Base


class Hifini(Base):
    web_key = 'hifini'
    web_url = 'https://www.hifini.com'

    def __init__(self):
        Base.__init__(self, self.web_url)

    def sign(self):
        try:
            res = True
            msg = '[' + self.web_key.upper() + '] 签到成功'
            # 读取cooke
            cookie = Base.get_cookie(self, self.web_key)

            # cookie不存在则进行登录
            if 0 == cookie['res']:
                Base.login_in(self, self.web_key, "//li[@class='nav-item username']")

            # 登录
            Base.sign(self, self.web_key)
            time.sleep(3)

            # 判断站点是否已签到
            is_sign = self.browser.find_element_by_xpath("//*[@id='sign']").text
            if '已签' != is_sign:
                # 签到
                Base.click(self, "//*[@id='start']")

            # 签到成功保存cookie
            Base.save_cookie(self, self.web_key)

            # 获取信息
            days = self.browser.find_element_by_xpath("//span[@id='day']").text
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
