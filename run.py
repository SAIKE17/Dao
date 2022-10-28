############
#  入口文件
############

import os
import sys
import time
import datetime
from api.log import Log
from api.mail import Mail
from website.hdtime import Hdtime
from website.hifini import Hifini
from website.pttime import Pttime
from website.lemon import Lemon
from website.smzdm import Smzdm
from website.mteam import Mteam
from website.btschool import Btschool

# 当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行
if __name__ == '__main__':
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()
    print('---- --------------------------------- ----')
    print('----- ----- ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ----- -----')
    print('------ ----------------------------- ------')

    print('当前执行:', sys.argv)

    # 动态引入模块 from website.hifini import Hifini 中的'website'
    import_module = __import__('website')

    # 动态引入模块 from website.hifini import Hifini 中的'hifini'
    web_class = getattr(import_module, sys.argv[1])

    # 加载模块中的类  from website.hifini import Hifini 中的'Hifini'
    web = getattr(web_class, sys.argv[1].capitalize())()

    # 执行签到
    res = web.sign()

    log = Log()
    # mail = Mail()

    # 记录日志并通知 TODO
