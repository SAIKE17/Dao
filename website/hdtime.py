# Encoding:UTF-8
# Project Name:Dao
# File:hdtime.py
# Created on:2021年12月17日 12:18:09 by kxl
#
import re
import time
import traceback

from .web_base import Base


class Hdtime(Base):
    web_key = 'hdt'
    web_url = 'https://hdtime.org'

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

            page = Base.get_page_source(self)
            # 获取信息
            check_in_value = re.findall(r"签到已得(.+?), 补签", page)
            if len(check_in_value) <= 0:
                # 签到
                Base.click(self, "//a[@href='attendance.php']")
                time.sleep(1)
                page = Base.get_page_source(self)
                check_in_times = re.findall(r"第 <b>(.+?)</b> 次签到", page)
                con_check_in_times = re.findall(r"连续签到 <b>(.+?)</b> 天", page)
                this_check_in_points = re.findall(r"获得 <b>(.+?)</b> 个魔力值", page)
                msg = msg + '\n' + '这是您的第' + str(check_in_times[0]) + '次签到，已连续签到' + str(con_check_in_times[0]) + '天，本次签到获得' + str(this_check_in_points[0]) + '魔力值'
            else:
                msg += '\n' + '签到已得：' + re.sub(r'[^\d.]', '', check_in_value[0])
            # 签到成功保存cookie
            Base.save_cookie(self, self.web_key)
            time.sleep(2)

            magic_value = re.findall(r"使用</a>]: (.+?)&nbsp;\(", page)
            if len(magic_value) <= 0:
                magic_value = re.findall(r"使用</a>]: (.+?) ", page)
            uploads = re.findall(r"上传量：</font>(.+?)<font", page)
            downloads = re.findall(r"下载量：</font> (.+?)<font", page)
            share_rate = re.findall(r"分享率：</font> (.+?)<font", page)
            msg += '\n' + '魔力值：' + re.sub(r'[^\d.]', '', magic_value[0] if len(magic_value) > 0 else '未获取')
            msg += '\n' + '上传量：' + re.sub(r'[^\d.]', '', uploads[0] if len(uploads) > 0 else '未获取') + ' GB'
            msg += '\n' + '下载量：' + re.sub(r'[^\d.]', '', downloads[0] if len(downloads) > 0 else '未获取') + ' GB'
            msg += '\n' + '分享率：' + re.sub(r'[^\d.]', '', share_rate[0] if len(share_rate) > 0 else '未获取')
        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
