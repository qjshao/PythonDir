# PythonDir
fiberhome meal auto signin
(公研餐卡签到)


【问题】
pkg_resources.DistributionNotFound: The 'APScheduler' distribution was not found and is required by the application

【解决方案】
1、新建hook-ctypes.macholib.py，内容
/***********************************************************************/
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    from PyInstaller.utils.hooks import copy_metadata

    datas = copy_metadata('apscheduler')
/***********************************************************************/
2、执行打包命令：pyinstaller -F MealSignIn.py --additional-hooks-dir=.

【问题】
[14880] Failed to execute script MealSignIn
Traceback (most recent call last):
  File "MealSignIn.py", line 106, in <module>
  File "site-packages\apscheduler\schedulers\base.py", line 411, in add_job
  File "site-packages\apscheduler\schedulers\base.py", line 905, in _create_trigger
  File "site-packages\apscheduler\schedulers\base.py", line 883, in _create_plugin_instance
  File "site-packages\pkg_resources\__init__.py", line 2291, in load
  File "site-packages\pkg_resources\__init__.py", line 2297, in resolve
ImportError: No module named cron

【解决方案】
待转换的python脚本MealSignIn.py中，加入如下代码：
from apscheduler.triggers import cron, interval
