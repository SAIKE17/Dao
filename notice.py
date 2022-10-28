# Encoding:UTF-8
# Project Name:Dao
# File:notice.py
# Created on:2022年06月20日 11:38:52 by SAIKE, 1059436959@qq.com
#
import datetime
from api.log import Log
from api.mail import Mail

# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
if __name__ == '__main__':
    print('---- --------------------------------- ----')
    print('----- ----- ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ----- -----')
    print('------ ----------------------------- ------')

    log = Log()
    mail = Mail()
    # TODO
