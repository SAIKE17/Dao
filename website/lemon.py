# Encoding:UTF-8
# Project Name:Dao
# File:lemon.py
# Created on:2021年12月20日 16:12:09 by SAIKE, 1059436959@qq.com
#
import re
import time
import traceback

from .web_base import Base


class Lemon(Base):
    web_key = 'lemon'
    web_url = 'https://lemonhd.org'

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
                Base.login_in(self, self.web_key, "//a[@href='logout.php']")

            # 登录
            Base.sign(self, self.web_key)
            time.sleep(3)
            # 签到判定
            is_sign = self.browser.find_element_by_id('dayBonusAvgId').text
            if '已签' != is_sign:
                self.browser.find_element_by_xpath("//a[@href='attendance.php']").click()
                # 签到面板
                sign_page = Base.get_page_source(self)
                check_in_times = re.findall(r"您的第 <b>(.+?)</b> 次签到", sign_page)
                con_check_in_times = re.findall(r"连续签到 <b>(.+?)</b> 天", sign_page)
                this_check_in_points = re.findall(r"签到获得 <b>(.+?)</b> 魔力值", sign_page)
                msg = msg + '\n' + '这是您的第' + str(check_in_times[0]) + '次签到，已连续签到' + str(con_check_in_times[0]) + '天，本次签到获得' + str(this_check_in_points[0]) + '魔力值'
            # 签到成功保存cookie
            Base.save_cookie(self, self.web_key)
            time.sleep(2)

            # 获取信息
            share_rate = self.browser.find_element_by_xpath("//table[@id='info_block']//table//table//tr[1]/td[5]").text
            uploads = self.browser.find_element_by_xpath("//table[@id='info_block']//table//table//tr[1]/td[7]").text
            magic_value = self.browser.find_element_by_xpath("//table[@id='info_block']//table//table//tr[1]/td[12]").text
            downloads = self.browser.find_element_by_xpath("//table[@id='info_block']//table//table//tr[2]/td[7]").text
            inbox = self.browser.find_element_by_xpath("//table[@id='info_block']//table//table//tr[2]/td[14]").text
            msg += '\n' + '当前' + magic_value[1:]
            msg += '\n' + '上传量：' + uploads
            msg += '\n' + '下载量：' + downloads
            msg += '\n' + '分享率：' + share_rate
            msg += '\n' + '收件箱：' + inbox

        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
