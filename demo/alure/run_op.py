# -*- coding:utf-8 -*-
import time

import pytest, os

pytest.main(['-s', 'test_report.py', '--alluredir', './temp'])
# 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
os.system('allure generate ./temp -o ./report --clean')
