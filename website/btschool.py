# Encoding:UTF-8
# Project Name:Dao
# File:btschool.py
# Created on:2022年01月22日 16:09:25 by SAIKE, 1059436959@qq.com
#
import time
import traceback

from .web_base import Base


class Btschool(Base):
    web_key = 'bts'
    web_url = 'https://pt.btschool.club'

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
            time.sleep(10)
            # 点击签到
            Base.click(self, "//a[@href='index.php?action=addbonus']")
            time.sleep(1)
            # 跳转到个人中心
            Base.click(self, "//a[@class='User_Name']")
            time.sleep(1)
            # 获取信息
            share_rate = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[1]/td[@class='embedded'][1]/font").text
            uploads = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[2]/td[@class='embedded'][1]").text
            downloads = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[2]/td[@class='embedded'][2]").text
            torrent_point = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='rowfollow']/table/tbody/tr[2]/td[@class='embedded'][3]").text
            magic_value = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='embedded']/table/tbody/tr[12]/td[@class='rowfollow']").text
            hr = self.browser.find_element_by_xpath("//table[@class='mainouter']//td[@class='embedded']/table/tbody/tr[18]/td[@class='rowfollow']").text
            msg += '\n' + '当前魔力值：' + magic_value
            msg += '\n' + uploads
            msg += '\n' + downloads.strip()
            msg += '\n' + torrent_point.strip()
            msg += '\n' + '分享率：' + share_rate
            msg += '\n' + 'H&R：' + hr
        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:            
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
