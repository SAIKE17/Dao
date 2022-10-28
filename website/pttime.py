# Encoding:UTF-8
# Project Name:Dao
# File:pttime.py
# Created on:2021年12月20日 16:11:43 by SAIKE, 1059436959@qq.com
#
import re
import time
import traceback

from .web_base import Base


class Pttime(Base):
    web_key = 'ptt'
    web_url = 'https://www.pttime.org'

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
            is_sign = self.browser.find_element_by_xpath("//a[@href='attendance.php']").text
            if '详情' != is_sign:
                # 点击签到
                self.browser.find_element_by_xpath("//a[@href='attendance.php']").click()
                # 签到面板
                sign_page = Base.get_page_source(self)
                check_in_times = re.findall(r"第 <b>(.+?)</b> 次签到", sign_page)
                con_check_in_times = re.findall(r"连续签到 <b>(.+?)</b> 天", sign_page)
                this_check_in_points = re.findall(r"获得 <b>(.+?)</b> 个魔力值", sign_page)
                msg = msg + '\n' + '这是你的第' + str(check_in_times[0]) + '次签到，已连续签到' + str(con_check_in_times[0]) + '天，本次签到获得' + str(this_check_in_points[0]) + '魔力值'
            # 签到成功保存cookie
            Base.save_cookie(self, self.web_key)
            time.sleep(2)

            # 获取信息
            page = Base.get_page_source(self)
            # 分享率
            share_rate = re.findall(r"分享率:</font>(.+?)<", page)
            # 上传
            uploads = re.findall(r"上传:</font>(.+?)<", page)
            # 下载
            downloads = re.findall(r"下载:</font>(.+?)<", page)
            # 魔力
            magic = re.findall(r"魔力值 \((.+?)\)", page)
            # 魔力值
            magic_value = re.findall(r"魔力说明</a>]: (.+?) <a", page)
            if len(magic_value) <= 0:
                magic_value = re.findall(r"魔力说明</a>]: (.+?)\(获", page)
            # 收件箱
            inbox = re.findall(r"收件箱:(.+?)</a>", page)
            msg += '\n' + '魔力值：' + magic_value[0] if len(magic_value) > 0 else '未获取'
            msg += '\n' + '魔力：' + magic[0] if len(magic) > 0 else '未获取'
            msg += '\n' + '上传量：' + uploads[0] if len(uploads) > 0 else '未获取'
            msg += '\n' + '下载量：' + downloads[0] if len(downloads) > 0 else '未获取'
            msg += '\n' + '分享率：' + share_rate[0] if len(share_rate) > 0 else '未获取'
            msg += '\n' + '收件箱：' + inbox[0] if len(inbox) > 0 else '未获取'
        except Exception as e:
            res = False
            msg = "[" + self.web_key.upper() + "] 执行异常:" + repr(e) + '\n'
            msg += traceback.format_exc()
            Base.save_page(self, self.web_key.upper() + '_error', self.browser.page_source)
        finally:
            return {"res": res, "msg": msg}

    def __del__(self):
        Base.__del__(self)
