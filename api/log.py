# 自定义系统日志
#
# 调用实例
# from .Log import Log
#
# api = Log()
# api.record(msg, met)
import datetime
import pytz
import os


class Log:
    def __init__(self):
        # 获取日期
        day = datetime.datetime.now(pytz.timezone('PRC')).strftime('%Y%m%d')
        # 获取上级目录
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        # 日志保存路径 root_path\api\year_day
        self.log_path = root_path + os.sep + "log" + os.sep + day[0:6]
        # 日志文件（按照日期分隔） root_path\api\year_month\day.api
        self.log_file = self.log_path + os.sep + day[6:8] + ".log"

    def read(self, file=0):
        if int(file) > 0:
            this_log_file = self.log_path + os.sep + file + ".log"
        else:
            this_log_file = self.log_file
        is_file = os.path.exists(this_log_file)
        if not is_file:
            return '文件不存在！'
        f = open(this_log_file, encoding='utf-8')
        log = f.read()
        f.close()
        return log

    def record(self, msg, met):
        # 判断路径是否存在
        is_file = os.path.exists(self.log_path)
        if not is_file:
            os.makedirs(self.log_path)

        log_msg = ''
        if isinstance(msg, str):
            log_msg = msg
        else:
            log_msg = str(msg, encoding='utf-8')

        f = open(self.log_file, "a+", encoding='utf-8')
        tm = datetime.datetime.now(pytz.timezone('PRC')).strftime('%Y-%m-%d %H:%M:%S')
        f.write(tm + '    ' + met + '    \n')
        f.write(log_msg + '\n')
        f.write('    \n')
        f.close()
