# Encoding:UTF-8
# Project Name:Dao
# File:mteam.py
# Created on:2021年12月25日 09:59:52 by SAIKE, 1059436959@qq.com
#
import time
import traceback

from .web_base import Base


class Mteam(Base):
    web_key = 'mt'
    web_url = 'https://kp.m-team.cc'

    def __init__(self):
        Base.__init__(self, self.web_url)

    def sign(self):
        try:
            res = True
            msg = '[' + self.web_key.upper() + '] 签到成功'

            # 读取cooke
            cookie = Base.get_cookie(self, self.web_key)

            # cookie不存在则进行登录
            if cookie['res'] is False:
                raise Exception(cookie['msg'])

            # 登录
            Base.sign(self, self.web_key)
            time.sleep(1)
            # 跳转到主页面
            self.browser.execute_script("window.open('" + self.web_url + "');")
            # 获取所有的窗口并跳转到新打开的窗口
            windows = self.browser.window_handles
            self.browser.switch_to.window(windows[1])
            Base.save_cookie(self, self.web_key)
            # 获取信息
            share_rate = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[1]/td[@class='embedded'][1]/font").text
            uploads = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[2]/td[@class='embedded'][1]").text
            magic_value = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='embedded']/table/tbody/tr[14]/td[@class='rowfollow']").text
            downloads = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='embedded']//td[@class='rowfollow']/table/tbody/tr[2]/td[@class='embedded'][2]").text
            inbox = self.browser.find_element_by_xpath("//table[@id='info_block']//td[@class='bottom'][2]/span[@class='medium']").text
            msg += '\n' + '当前魔力值：' + magic_value
            msg += '\n' + uploads
            msg += '\n' + downloads.strip()
            msg += '\n' + '分享率：' + share_rate
            msg += '\n' + '收件箱：' + inbox.replace('\n', ' | ').replace('\r', ' | ')
        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
