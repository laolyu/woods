# -*- coding:utf-8 -*-
import os
import re
import time
import allure
import pytest
import yagmail
from bdocr import domain
import urllib3
import random
from loguru import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@allure.feature('签到')
class TestDd:
    def setup_method(self):
        logger.debug('start')

    def teardown_method(self):
        os.system('adb shell input keyevent 3')
        logger.debug('end')

    # @pytest.fixture()
    @allure.story('设备在线')
    def test_devices(self):
        sleeptime = random.randint(0, 300)
        time.sleep(sleeptime)
        # os.system('adb devices')  # power
        result = os.popen('adb devices')
        context = result.read()
        assert '022GPLDU39019379' in context

    @pytest.fixture()
    def file(self):
        logger.info('截图-------')
        file = r'F:\screenshot\screenshot.png'
        try:
            os.remove(file)
        except OSError as e:
            logger.info(e)
        time.sleep(2)
        os.system('adb shell input keyevent 26')  # power
        time.sleep(2)
        os.system('adb shell input keyevent 3')  # home
        time.sleep(2)
        logger.debug('DD-start')
        os.system('adb shell monkey -p com.alibaba.android.rimet 1')  # start
        sleeptime = random.randint(25, 40)
        time.sleep(sleeptime)
        logger.debug('screenshot')
        os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        time.sleep(2)
        os.system('adb pull /sdcard/screenshot.png F:/screenshot')
        os.system('adb shell am force-stop com.alibaba.android.rimet')
        return file

    @pytest.fixture()
    def message(self, file):
        messages = domain(file)
        message = messages.replace('考勤打卡:', '').replace('钉钉', '').replace('设置工作状态Q搜索', '').replace('M工作通知:上海展盟网', '')
        return message

    @pytest.fixture()
    def subject(self, message):
        subject = ''
        pattern = re.compile(r'\d{2}:\d{2}极速打卡成功')
        it = pattern.findall(message)

        pattern_on = re.compile(r'\d{2}:\d{2}.班打卡')
        it_on = pattern_on.findall(message)

        if it:
            subject = it[0]
        elif it_on:
            subject = it_on[0]
        return subject

    @allure.story('检查并发邮件')
    @pytest.mark.flaky(reruns=3, reruns_delay=20)
    def test_todo(self, file, subject, message):
        assert subject != ''

        receiver = "pytest@139.com"
        yag = yagmail.SMTP("laolyu@foxmail.com", 'okpykwvdqeczhage', 'smtp.qq.com')
        yag.send(
            to=receiver,
            subject=subject,
            contents=message,
            attachments=file,
        )
        logger.info('subject=%s,message=%s' % (subject, message))


if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', './temp'])
    os.system('allure generate ./temp -o ./report --clean')
